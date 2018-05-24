# -*- coding: utf-8 -*-
from dataProcess.dap.modules import functions


def translate_alias(string, scope=""):
    string = functions.translate_full_shaped_to_half(string)
    string = functions.complex_font_to_simple_font(string)
    if scope:
        string = functions.translate_hash_table(string, scope)
    return string

if __name__ == '__main__':
    print(translate_alias('每重毫', 's'))  # 每重毫
    print(translate_alias('水蜜丸每40丸重3g', 's'))  # 水蜜剂每40剂重3g
    print(translate_alias('洛克35克', 's'))  # 洛g35g
    print(translate_alias('水蜜丸每40丸', 's'))  # 水蜜剂每40剂
    print(translate_alias('、lL０.３１ｇ', 'w'))  # ;lL0.31g
    print(translate_alias('维生素Ｃ注射液'))  # 维生素C注射液
    print(translate_alias('繁體字，繁體中文的叫法在臺灣亦很常見。'))  # 繁体字,繁体中文的叫法在台湾亦很常见。

