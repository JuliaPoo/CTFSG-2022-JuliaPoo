from gen_nums import *
import pickle, os

def _load_nums():
    c = "_cache/nums.pickle.55"
    nums = pickle.load(open(c, 'rb'))
    return [n[0] for n,_ in nums]

nums:str = _load_nums()

#func_to_int:str = "[n: n(A)(0)]"
#func_to_bool:str = "[b: b(0)(1)]"

# n = nums[255]
# print(f"{func_to_int}({n})")
# print(eval(f"{func_to_int}({n})"))