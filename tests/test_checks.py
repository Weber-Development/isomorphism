from isomorphism._checks import ahv_ok, iban_ok, uid_ok


def test_ahv() -> None:
    assert ahv_ok("7561234567897")
    assert not ahv_ok("7561234567898")  # wrong check digit
    assert not ahv_ok("7551234567897")  # wrong prefix
    assert not ahv_ok("756123456789")  # too short


def test_iban() -> None:
    assert iban_ok("CH9300762011623852957")
    assert iban_ok("LI21088100002324013AA")
    assert not iban_ok("CH9300762011623852958")
    assert not iban_ok("CH93")


def test_uid() -> None:
    assert uid_ok("123456788")
    assert not uid_ok("123456789")
    assert not uid_ok("12345678")
    assert not uid_ok("100000007")  # mod-11 check would be 10, never valid
