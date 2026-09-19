# fake_modules_py
pip is not working? well heres some modules!
## requests

```
import sys, os        
     
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))  

import requests  # now resolves from vendor/
 ```
## this is wip
there are like 2 use cases for this and for the first couple modules im using claude, then i'll rewrite and write my own
