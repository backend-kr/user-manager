from model_utils import Choices


class ProfileChoices:
    MOBILE_CARRIER = Choices(
        ('01', 'skt', 'SKT'),
        ('02', 'kt', 'KT'),
        ('03', 'lg', 'LG U+'),
        ('알뜰폰', [
            ('04', 'r_skt', 'SKT'),
            ('05', 'r_kt', 'KT'),
            ('06', 'r_lg', 'LG U+')
        ]),
    )

    GENDER_TYPE = Choices(
        ('내국인', [
            (1, 'l1', '남(1)'),
            (2, 'l2', '여(2)'),
        ]),
        ('외국인', [
            (3, 'f3', '남(3)'),
            (4, 'f4', '여(4)'),
        ])
    )