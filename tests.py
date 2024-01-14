import metric

assert metric.report_success_LLM('1 2  4 5', 'Count from 1 to 5') == False

assert metric.report_success_LLM('1 2 2 4 5', 'Count from 1 to 5') == False

assert metric.report_success_LLM('1 2 3 4 5', 'Count from 1 to 5') == True

assert metric.report_success_LLM('1 2 three 4 5', 'Count from 1 to 5') == True