# -*- coding: utf-8 -*-
import unittest
from dataProcess.dap.dataAnalysis.clinic_extra_term import *


class ClinicExtraTermTestCase(unittest.TestCase):

    def test_is_element_increment(self):
        nums = [13, 1, 2, 3, 5, 7, 8, 9, 14, 1, 2, 3, 15]
        res = [[1, 2, 3], [7, 8, 9], [1, 2, 3]]
        self.assertEqual(is_element_increment(nums), res)

    def test_extract_clinic_term(self):
        m = extract_clinic_term
        self.assertEqual(m('13tang1.AB2.DF3们;发炎?PICC封管;5ha;7感冒8流感9突发性感冒14+6周1为2qq3eeds'),
                         '13tang||1||.AB||2||.DF||3||们||发炎||PICC封管||5ha||7||感冒||8||流感||9||突发性感冒14+6周'
                         '||1||为||2||qq||3||eeds')
        self.assertEqual(m('传染性单核细胞增多症'),
                         '传染性单核细胞增多症')
        self.assertEqual(m('46死髓;27隐裂牙髓炎'),
                         '46死髓||27隐裂牙髓炎')

if __name__ == '__main__':
    unittest.main()

