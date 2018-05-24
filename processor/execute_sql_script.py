# -*- coding: utf-8 -*-

from dataProcess.dap.modules.script import Script

script = Script()
output = script.execute_sql_script('test.sql')
print(output)



