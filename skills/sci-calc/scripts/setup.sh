#!/bin/bash
# 과학 계산 라이브러리 설치 (환경이 대화마다 초기화되므로 매번 실행)
pip install CoolProp cantera pint fluids ht --break-system-packages -q 2>&1 | grep -v -i "warning" | tail -2
python3 -c "
import CoolProp, cantera, pint, fluids, ht, numpy, scipy, sympy
print('ready: CoolProp', CoolProp.__version__, '| Cantera', cantera.__version__, '| pint', pint.__version__, '| fluids', fluids.__version__, '| ht', ht.__version__)
"
