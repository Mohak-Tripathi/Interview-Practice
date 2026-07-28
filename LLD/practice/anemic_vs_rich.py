"""
ANEMIC DOMAIN MODEL vs RICH DOMAIN MODEL  —  Python translation
================================================================
Original article (Kotlin): Matthias Schenk
    https://medium.com/@inzuael/anemic-domain-model-vs-rich-domain-model-78752b46098f

This file replicates the article's code in Python, verbatim in intent, with
extra comments that (a) explain the Kotlin idioms you didn't recognise and
(b) point out exactly where behaviour moves between the two approaches.

HOW TO READ THIS FILE
    Part 0  DTOs                (shared by both approaches)
    Part 1  ANEMIC             dumb data + fat service   <- how you build today
    Part 2  RICH               smart objects + thin service   <- the LLD/DDD way
    Part 3  runnable demo      run `python anemic_vs_rich.py` to see both

KOTLIN -> PYTHON CHEAT SHEET (referenced throughout)
    data class            -> @dataclass  (add frozen=True for immutability)
    sealed interface      -> ABC base class + fixed set of subclasses
    require(cond){ "msg" } -> if not cond: raise ValueError("msg")
    companion object fun  -> @classmethod  (a factory that builds the object)
    init { ... } block    -> __post_init__(self)  (runs right after construction)
    copy(field = new)     -> dataclasses.replace(obj, field=new)
    DTO                   -> "Data Transfer Object": a plain bag of fields used
                             to carry request input INTO the system. It has no
                             behaviour and no rules. It is NOT the domain model.
                             You already create these every time you accept a
                             JSON request body — you just never named them.
"""

from __future__ import annotations
import re
import uuid
from abc import ABC
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import List, Optional


# =============================================================================
# PART 0 — DTOs  (Data Transfer Objects)   [shared by BOTH approaches]
# =============================================================================
# In Kotlin these were `data class`. A data class auto-generates equality,
# hashing and a copy() method, and is treated as a value (two objects with the
# same fields are "equal"). Python's @dataclass does the same thing.
#
# frozen=True makes them immutable (like Kotlin `val` fields) — you cannot
# reassign a field after creation. The article relies on immutability, so we
# keep it.
#
# THE POINT OF A DTO: it is the shape of the INPUT. The user of the service
# hands you a DTO; the service turns it into a real domain object. Keeping DTO
# and domain model separate means the outside world can't hand you a
# half-built domain object.

@dataclass(frozen=True)
class UserDto:
    username: str
    password: str


@dataclass(frozen=True)
class ContactDetailsDto:
    street: str
    street_number: str
    zip_code: int
    city: str


# ---- Kotlin `sealed interface PaymentInformationDto` ----
# A "sealed" type means: there is a FIXED, known set of subtypes and no others.
# Kotlin uses this so a `when` (switch) over the subtypes is exhaustive.
# Python has no sealed keyword, so we approximate: an abstract base class (ABC)
# with exactly three concrete subclasses. The `id` field is shared by all.
class PaymentInformationDto(ABC):
    id: uuid.UUID


@dataclass(frozen=True)
class PaypalPaymentInformationDto(PaymentInformationDto):
    id: uuid.UUID
    mail_address: str


@dataclass(frozen=True)
class BankPaymentInformationDto(PaymentInformationDto):
    id: uuid.UUID
    iban: str
    owner: str


@dataclass(frozen=True)
class CreditCardPaymentInformationDto(PaymentInformationDto):
    id: uuid.UUID
    number: str
    owner: str
    security_number: int


@dataclass(frozen=True)
class TransactionDto:
    amount: float
    items: List[str]


# =============================================================================
# Shared domain value types (used by both approaches)
# =============================================================================
class TransactionType(Enum):
    BUY = "BUY"
    RETOURE = "RETOURE"   # "retoure" = a return/refund transaction


# Validation constants + regexes (identical rules to the article)
MINIMUM_PASSWORD_LENGTH = 16
LOWERCASE_RE = re.compile(r"[a-z]+")
UPPERCASE_RE = re.compile(r"[A-Z]+")
SPECIAL_RE = re.compile(r"[!&%?<>\-]+")
IBAN_RE = re.compile(r"^DE[0-9]{20}$")
CREDIT_CARD_RE = re.compile(r"^[0-9]{4}([ -]?[0-9]{4}){3}$")
# NOTE: the article's paypal regex was garbled in the source HTML. This is a
# sane equivalent of "looks like an email".
EMAIL_RE = re.compile(r"^[A-Za-z].*@.+\..+$")


# #############################################################################
#
#   PART 1 — ANEMIC DOMAIN MODEL
#   dumb data holders + ALL logic in the service
#   (this is the shape your ORM + service layer produces today)
#
# #############################################################################

# ---- Anemic domain model: pure data, ZERO behaviour ----
# Compare these to the DTOs above — they're almost identical. That's the whole
# smell: the "domain model" is just another data bag. It knows nothing about
# the rules that govern it. Anyone can construct an INVALID User.

@dataclass(frozen=True)
class ContactDetails:
    street: str
    street_number: str
    zip_code: int
    city: str


class PaymentInformation(ABC):
    id: uuid.UUID


@dataclass(frozen=True)
class PaypalPaymentInformation(PaymentInformation):
    id: uuid.UUID
    mail_address: str


@dataclass(frozen=True)
class BankPaymentInformation(PaymentInformation):
    id: uuid.UUID
    iban: str
    owner: str


@dataclass(frozen=True)
class CreditCardPaymentInformation(PaymentInformation):
    id: uuid.UUID
    number: str
    owner: str
    security_number: int


@dataclass(frozen=True)
class Transaction:
    transaction_type: TransactionType
    amount: float
    items: List[str]


@dataclass(frozen=True)
class AnemicUser:
    """A data holder. No methods. No rules. It CANNOT protect itself from
    being created in an invalid state — that's the service's job below."""
    username: str
    password: str
    contact_details: ContactDetails
    payment_information: List[PaymentInformation]
    transactions: List[Transaction] = field(default_factory=list)


# ---- Repository interface (persistence boundary) ----
# In Kotlin this was `interface UserRepository`. Python has no interface
# keyword; the idiomatic equivalent is an ABC with unimplemented methods.
# The repository is the ONLY thing that talks to storage. Even in the anemic
# version this boundary exists — the service does NOT do SQL directly.
class AnemicUserRepository(ABC):
    def is_username_already_used(self, username: str) -> bool: ...
    def save(self, user: AnemicUser) -> AnemicUser: ...
    def find_by(self, username: str) -> Optional[AnemicUser]: ...
    def update(self, user: AnemicUser) -> AnemicUser: ...


class AnemicUserService:
    """
    THE FAT SERVICE. Every business rule lives here:
        - username uniqueness
        - password validation
        - contact-detail validation
        - payment-info validation
        - mapping DTO -> domain object
    The AnemicUser is passive; this service reaches in and decides everything.
    This is the anti-pattern Fowler named: the object has a domain name but
    none of the domain behaviour.
    """

    def __init__(self, repository: AnemicUserRepository):
        self._repository = repository

    def create_user(
        self,
        user_dto: UserDto,
        contact_dto: ContactDetailsDto,
        payment_dto: PaymentInformationDto,
    ) -> AnemicUser:
        # --- ALL validation happens out here, in the caller ---
        if self._repository.is_username_already_used(user_dto.username):
            raise ValueError(f"User with username '{user_dto.username}' already exists.")
        self._validate_password(user_dto.password)
        self._validate_contact_details(contact_dto)
        self._validate_payment_information(payment_dto)

        user = self._map_to_user(user_dto, contact_dto, payment_dto)
        return self._repository.save(user)

    # DTO -> domain mapping also lives in the service
    def _map_to_user(self, user_dto, contact_dto, payment_dto) -> AnemicUser:
        return AnemicUser(
            username=user_dto.username,
            password=user_dto.password,
            contact_details=ContactDetails(
                street=contact_dto.street,
                street_number=contact_dto.street_number,
                zip_code=contact_dto.zip_code,
                city=contact_dto.city,
            ),
            payment_information=[_dto_to_payment_anemic(payment_dto)],
        )

    # Kotlin `require(cond) { "msg" }` == "if not cond, throw with this message".
    # It's just a guard clause. Below is the literal Python equivalent.
    def _validate_password(self, password: str) -> None:
        if not len(password) >= MINIMUM_PASSWORD_LENGTH:
            raise ValueError(
                f"Password (current: {len(password)}) must be at minimum "
                f"{MINIMUM_PASSWORD_LENGTH} characters long."
            )
        if not LOWERCASE_RE.search(password):
            raise ValueError("Password must contain at minimum 1 lowercase character.")
        if not UPPERCASE_RE.search(password):
            raise ValueError("Password must contain at minimum 1 uppercase character.")
        if not SPECIAL_RE.search(password):
            raise ValueError("Password must contain at minimum 1 special character of (!&%?<>-).")

    def _validate_contact_details(self, c: ContactDetailsDto) -> None:
        if not c.street_number:
            raise ValueError("Street number must not be empty.")
        if not c.street:
            raise ValueError("Street must not be empty.")
        if not (10000 <= c.zip_code <= 99999):
            raise ValueError("Zip code must be within range of 10.000 to 99.999.")
        if not c.city:
            raise ValueError("City must not be empty.")

    # Kotlin used `when (dto) { is Bank -> ...; is Credit -> ...; is Paypal -> ... }`
    # — an exhaustive switch over the sealed subtypes. Python: isinstance checks.
    # (On Python 3.10+ you could use `match dto: case BankPaymentInformationDto():`)
    def _validate_payment_information(self, dto: PaymentInformationDto) -> None:
        if isinstance(dto, BankPaymentInformationDto):
            if not IBAN_RE.match(dto.iban):
                raise ValueError("IBAN has not the correct format.")
            if not dto.owner:
                raise ValueError("Bank owner must not be empty.")
        elif isinstance(dto, CreditCardPaymentInformationDto):
            if not CREDIT_CARD_RE.match(dto.number):
                raise ValueError("Credit card number has not the correct format.")
            if not dto.owner:
                raise ValueError("Credit card owner must not be empty.")
        elif isinstance(dto, PaypalPaymentInformationDto):
            if not EMAIL_RE.match(dto.mail_address):
                raise ValueError("Mail address has not the correct format.")
        else:
            raise ValueError("Unknown payment information type.")


def _dto_to_payment_anemic(dto: PaymentInformationDto) -> PaymentInformation:
    """DTO -> domain object mapping for the anemic side.
    In Kotlin this was an extension function `dto.toPaymentInformation()`."""
    if isinstance(dto, PaypalPaymentInformationDto):
        return PaypalPaymentInformation(id=dto.id, mail_address=dto.mail_address)
    if isinstance(dto, BankPaymentInformationDto):
        return BankPaymentInformation(id=dto.id, iban=dto.iban, owner=dto.owner)
    if isinstance(dto, CreditCardPaymentInformationDto):
        return CreditCardPaymentInformation(
            id=dto.id, number=dto.number, owner=dto.owner,
            security_number=dto.security_number,
        )
    raise ValueError("Unknown payment DTO type.")


# #############################################################################
#
#   PART 2 — RICH DOMAIN MODEL
#   smart object (owns data + rules + use-cases) + THIN service
#   (this is the DDD / LLD-interview shape)
#
# #############################################################################

# The article pulled password validation into its OWN object so the User class
# doesn't grow huge. In Kotlin this was `object PasswordValidator` (a
# singleton). Python equivalent: a class with a @staticmethod, or just a
# module-level function. A staticmethod keeps the name grouped, like Kotlin.
class PasswordValidator:
    @staticmethod
    def validate(password: str) -> None:
        if not len(password) >= MINIMUM_PASSWORD_LENGTH:
            raise ValueError(
                f"Password (current: {len(password)}) must be at minimum "
                f"{MINIMUM_PASSWORD_LENGTH} characters long."
            )
        if not LOWERCASE_RE.search(password):
            raise ValueError("Password must contain at minimum 1 lowercase character.")
        if not UPPERCASE_RE.search(password):
            raise ValueError("Password must contain at minimum 1 uppercase character.")
        if not SPECIAL_RE.search(password):
            raise ValueError("Password must contain at minimum 1 special character of (!&%?<>-).")


@dataclass(frozen=True)
class RichUser:
    """
    THE RICH DOMAIN MODEL.

    Difference #1 — it validates itself on construction (__post_init__ ==
    Kotlin's `init {}` block). It is now IMPOSSIBLE to hold an invalid RichUser.
    In the anemic version, validity depended on remembering to call the service.

    Difference #2 — the use-cases (update password, add payment, add
    transaction, ...) are METHODS ON THIS OBJECT, not functions in a service.
    The knowledge of "how a user changes" lives with the user.

    Note on immutability: the article's design is immutable — every "update"
    returns a NEW user rather than mutating in place (Kotlin `copy()`).
    Python equivalent: dataclasses.replace(). This is a style choice, not a
    requirement of rich models; a mutable rich object is equally valid. Kept
    faithful to the article.
    """
    username: str
    password: str
    contact_details: ContactDetails
    payment_information: List[PaymentInformation]
    transactions: List[Transaction] = field(default_factory=list)

    # Kotlin `init { ... }` -> Python `__post_init__`. Runs immediately after
    # the object is built. This is where the object guards its OWN validity.
    def __post_init__(self):
        PasswordValidator.validate(self.password)
        if not self.payment_information:
            raise ValueError("There must be at minimum one payment information available.")

    # ---- Factory: Kotlin `companion object { fun createFrom(...) }` ----
    # A @classmethod that builds the object from DTOs. In the article the
    # constructor is made private so creation MUST go through this factory,
    # giving one controlled entry point. Python can't truly hide __init__, but
    # the convention is: "build RichUsers via create_from()."
    @classmethod
    def create_from(
        cls,
        user_dto: UserDto,
        contact_dto: ContactDetailsDto,
        payment_dto: PaymentInformationDto,
    ) -> "RichUser":
        return cls(
            username=user_dto.username,
            password=user_dto.password,
            contact_details=ContactDetails(
                street=contact_dto.street,
                street_number=contact_dto.street_number,
                zip_code=contact_dto.zip_code,
                city=contact_dto.city,
            ),
            payment_information=[_dto_to_payment_rich(payment_dto)],
        )

    # ---- Use-cases as behaviour ON the object ----
    # Each returns a new RichUser (copy-on-write via replace()). Because the
    # returned object re-runs __post_init__, an update can never produce an
    # invalid user either.

    def update_password(self, new_password: str) -> "RichUser":
        return replace(self, password=new_password)

    def update_street(self, new_street: str) -> "RichUser":
        return replace(self, contact_details=replace(self.contact_details, street=new_street))

    def update_street_number(self, new_number: str) -> "RichUser":
        return replace(self, contact_details=replace(self.contact_details, street_number=new_number))

    def update_city(self, new_city: str) -> "RichUser":
        return replace(self, contact_details=replace(self.contact_details, city=new_city))

    def update_zip_code(self, new_zip: int) -> "RichUser":
        return replace(self, contact_details=replace(self.contact_details, zip_code=new_zip))

    def add_paypal_payment(self, mail_address: str) -> "RichUser":
        new_pi = self.payment_information + [
            PaypalPaymentInformation(id=uuid.uuid4(), mail_address=mail_address)
        ]
        return replace(self, payment_information=new_pi)

    def add_bank_payment(self, iban: str, owner: str) -> "RichUser":
        new_pi = self.payment_information + [
            BankPaymentInformation(id=uuid.uuid4(), iban=iban, owner=owner)
        ]
        return replace(self, payment_information=new_pi)

    def add_credit_card_payment(self, number: str, owner: str, security_number: int) -> "RichUser":
        new_pi = self.payment_information + [
            CreditCardPaymentInformation(
                id=uuid.uuid4(), number=number, owner=owner, security_number=security_number
            )
        ]
        return replace(self, payment_information=new_pi)

    def remove_payment_information(self, payment_information_id: uuid.UUID) -> "RichUser":
        new_pi = [p for p in self.payment_information if p.id != payment_information_id]
        return replace(self, payment_information=new_pi)

    def add_transaction(self, amount: float, items: List[str]) -> "RichUser":
        # The RULE "positive amount = BUY, else RETOURE" lives INSIDE the user.
        # In the anemic version this rule would sit in the service.
        tx = Transaction(
            transaction_type=TransactionType.BUY if amount > 0 else TransactionType.RETOURE,
            amount=amount,
            items=items,
        )
        return replace(self, transactions=self.transactions + [tx])


def _dto_to_payment_rich(dto: PaymentInformationDto) -> PaymentInformation:
    if isinstance(dto, PaypalPaymentInformationDto):
        return PaypalPaymentInformation(id=dto.id, mail_address=dto.mail_address)
    if isinstance(dto, BankPaymentInformationDto):
        return BankPaymentInformation(id=dto.id, iban=dto.iban, owner=dto.owner)
    if isinstance(dto, CreditCardPaymentInformationDto):
        return CreditCardPaymentInformation(
            id=dto.id, number=dto.number, owner=dto.owner,
            security_number=dto.security_number,
        )
    raise ValueError("Unknown payment DTO type.")


# ---- Rich repository: note getBy returns a User (not Optional) ----
# The article moved the "missing user" handling INTO the repository, so the
# thin service never has to check for None. Small but deliberate: push the
# not-found concern to the persistence boundary.
class RichUserRepository(ABC):
    def is_username_already_used(self, username: str) -> bool: ...
    def save(self, user: RichUser) -> RichUser: ...
    def get_by(self, username: str) -> RichUser: ...       # raises if missing
    def update(self, user: RichUser) -> RichUser: ...


class RichUserService:
    """
    THE THIN SERVICE. Look how little is here now. It does exactly three
    things per use-case: load (repo) -> tell the object to change itself ->
    save (repo). No validation, no rules, no DTO-mapping decisions — all of
    that moved DOWN into RichUser. This is "thin orchestrator over rich model".
    """

    def __init__(self, repository: RichUserRepository):
        self._repository = repository

    def create_user(self, user_dto, contact_dto, payment_dto) -> RichUser:
        user = RichUser.create_from(user_dto, contact_dto, payment_dto)  # validates itself
        return self._repository.save(user)

    def update_password(self, username: str, password: str) -> RichUser:
        user = self._repository.get_by(username)
        return self._repository.update(user.update_password(password))

    def update_contact_details(self, username: str, contact_dto: ContactDetailsDto) -> RichUser:
        user = self._repository.get_by(username)
        # method chaining works because each update returns a new RichUser
        updated = (
            user.update_street(contact_dto.street)
                .update_street_number(contact_dto.street_number)
                .update_city(contact_dto.city)
                .update_zip_code(contact_dto.zip_code)
        )
        return self._repository.update(updated)

    def add_payment_information(self, username: str, payment_dto: PaymentInformationDto) -> RichUser:
        user = self._repository.get_by(username)
        if isinstance(payment_dto, PaypalPaymentInformationDto):
            updated = user.add_paypal_payment(payment_dto.mail_address)
        elif isinstance(payment_dto, BankPaymentInformationDto):
            updated = user.add_bank_payment(payment_dto.iban, payment_dto.owner)
        elif isinstance(payment_dto, CreditCardPaymentInformationDto):
            updated = user.add_credit_card_payment(
                payment_dto.number, payment_dto.owner, payment_dto.security_number
            )
        else:
            raise ValueError("Unknown payment information type.")
        return self._repository.update(updated)

    def remove_payment_information(self, username: str, payment_information_id: uuid.UUID) -> RichUser:
        user = self._repository.get_by(username)
        return self._repository.update(user.remove_payment_information(payment_information_id))

    def add_transaction(self, username: str, transaction_dto: TransactionDto) -> RichUser:
        user = self._repository.get_by(username)
        return self._repository.update(user.add_transaction(transaction_dto.amount, transaction_dto.items))


# #############################################################################
#
#   PART 3 — RUNNABLE DEMO  (NOT in the original article)
#   The article left repositories as empty interfaces. To let you actually RUN
#   this and feel the difference, here are trivial in-memory implementations
#   (a dict standing in for a database) and a small script.
#
# #############################################################################

class InMemoryAnemicUserRepository(AnemicUserRepository):
    def __init__(self):
        self._store: dict[str, AnemicUser] = {}
    def is_username_already_used(self, username): return username in self._store
    def save(self, user): self._store[user.username] = user; return user
    def find_by(self, username): return self._store.get(username)
    def update(self, user): self._store[user.username] = user; return user


class InMemoryRichUserRepository(RichUserRepository):
    def __init__(self):
        self._store: dict[str, RichUser] = {}
    def is_username_already_used(self, username): return username in self._store
    def save(self, user): self._store[user.username] = user; return user
    def get_by(self, username):
        if username not in self._store:
            raise ValueError(f"User '{username}' not found.")   # not-found handled HERE
        return self._store[username]
    def update(self, user): self._store[user.username] = user; return user


if __name__ == "__main__":
    valid_pw = "MyPassword!123456"          # 17 chars, upper+lower+special -> valid
    contact = ContactDetailsDto("Main Street", "42", 50667, "Cologne")
    paypal = PaypalPaymentInformationDto(id=uuid.uuid4(), mail_address="a@b.com")

    print("=" * 60)
    print("ANEMIC: service validates, object is a passive bag")
    print("=" * 60)
    anemic_service = AnemicUserService(InMemoryAnemicUserRepository())
    u1 = anemic_service.create_user(UserDto("alice", valid_pw), contact, paypal)
    print("created:", u1.username, "| pw ok because the SERVICE checked it")
    # The danger the article warns about: nothing stops you building an INVALID
    # anemic user directly, bypassing the service entirely:
    invalid = AnemicUser("bob", "short", ContactDetails("s", "1", 50667, "C"), [])
    print("BYPASSED service -> invalid user exists anyway:", invalid.username,
          "| password:", repr(invalid.password), "(too short, no rule stopped it)")

    print()
    print("=" * 60)
    print("RICH: object validates ITSELF, cannot exist invalid")
    print("=" * 60)
    rich_service = RichUserService(InMemoryRichUserRepository())
    r1 = rich_service.create_user(UserDto("alice", valid_pw), contact, paypal)
    print("created:", r1.username)
    # use-case runs on the object; returns a NEW user (immutable copy-on-write)
    r2 = rich_service.add_transaction("alice", TransactionDto(amount=99.0, items=["book"]))
    print("after add_transaction -> tx type decided BY the object:",
          r2.transactions[0].transaction_type.name)
    # Try to build an invalid rich user directly -> the object refuses:
    try:
        RichUser("bob", "short", ContactDetails("s", "1", 50667, "C"), [])
    except ValueError as e:
        print("tried to build invalid RichUser directly -> REJECTED:", e)