import nn2nfa.translation.automata_builder as builder

import unittest
import random as ran
import time
import math

class AutomataTest(unittest.TestCase):
    def test_signed_mult(self):
        for _ in range(5):
            a = ran.randint(-10000, 10000)
            print(f"Building automaton for multiplication with {a}")
            start = time.time()
            mult_automaton = builder.build_signed_multiplier(a)
            end = time.time()
            #print(mult_automaton.graph)
            print(f"Built in {end - start} s")

            for _ in range(5):
                ex = ran.randint(0, 1)
                b = ran.randint(-10000, 10000)
                b_bin = bin(int(abs(b))).split('b')[1][::-1]
                b_bin = "1"+b_bin if b < 0 else "0"+b_bin
                res_bin = bin(int(abs((a*b)+(1-ex)))).split('b')[1][::-1]
                res_bin = "1" + res_bin if a*b < 0 else "0" + res_bin
                test_w = []
                for i in range(len(res_bin)):
                    a_bit = 0
                    if i < len(b_bin):
                        a_bit = b_bin[i]
                    test_w.append(str(a_bit)+str(res_bin[i]))

                print(f"# Testing {a}*{b}. With {bool(ex)} example")
                res = int(mult_automaton.test(test_w))
                assert res == ex
                print(f"Result: {res}")

    def test_n_adder(self):
        for i in range(3, 20):
            # Generate signs
            signs = [ran.randint(0, 1) for _ in range(i)]
            res_sign = ran.randint(0, 1)
            bias = ran.randint(-9999, 9999)
            automaton = builder.build_n_adder(i, signs, res_sign, bias)
            print(f"Testing {i}-Adder with {res_sign} result, bias={bias} and signs={signs}")
            for _ in range(500):
                false_ex = bool(ran.randint(0, 1))
                z_list = []
                z_bin_list = []
                for j in range(i):
                    z = ran.randint(0, 100000)
                    z_bin = bin(int(abs(z))).split('b')[1][::-1]
                    #z_bin = "1" + z_bin if z < 0 else "0" + z_bin
                    if signs[j] == 1:
                        z = -z
                    z_list.append(z)
                    z_bin_list.append(z_bin)

                if not false_ex:
                    res = sum(z_list) + bias
                else:
                    res = sum(z_list) + bias + ran.randint(1, 1000)
                if not ((res < 0 and res_sign == 1) or (res >= 0 and res_sign == 0)):
                    continue
                res_bin = bin(int(abs(res))).split('b')[1][::-1]
                #res_bin = "1" + res_bin if res < 0 else "0" + res_bin
                z_bin_list.append(res_bin)

                max_len = math.ceil(math.log2(i*max([abs(z) for z in z_list]))+1)
                z_bin_list = [z_bin.ljust(max_len, '0') for z_bin in z_bin_list]

                print(f"sum({z_list}) = {res}")
                print(f"Test { not false_ex} Example")
                test_w = []

                for j in range(max_len):
                    w_list = []
                    for w in z_bin_list:
                        w_list.append(w[j])
                    test_w.append("".join(w_list))

                print(f"Testing {test_w}")
                res = automaton.test(test_w)
                if false_ex:
                    assert not res
                else:
                    assert res
                print(f"Result: {res}")

    def test_n_multiplier(self):
        for i in range(2, 6):
            weights = [ran.randint(-3, 3) for _ in range(i)]
            automaton = builder.build_n_multiplier(weights)
            print(f"Testing {i}-Multiplier with {weights}")
            for _ in range(500):
                false_ex = bool(ran.randint(0, 1))
                z_list = []
                z_bin_list = []
                for j in range(i):
                    z = ran.randint(-100, 100)
                    z_bin = bin(int(abs(z))).split('b')[1][::-1]
                    z_bin = "1" + z_bin if z < 0 else "0" + z_bin
                    z_list.append(z)
                    z_bin_list.append(z_bin)

                for j in range(i):
                    if not false_ex:
                        res = weights[j] * z_list[j]

                    else:
                        res = weights[j] * z_list[j] + ran.randint(1, 1000)
                    res_bin = bin(int(abs(res))).split('b')[1][::-1]
                    res_bin = "1" + res_bin if res < 0 else "0" + res_bin
                    z_list.append(res)
                    z_bin_list.append(res_bin)

                max_len = math.ceil(math.log2(i * max([abs(z) for z in z_list])) + 1)
                z_bin_list = [z_bin.ljust(max_len, '0') for z_bin in z_bin_list]

                print(f"mult({z_list})")
                print(f"Test {not false_ex} Example")
                test_w = []

                for j in range(max_len):
                    w_list = []
                    for w in z_bin_list:
                        w_list.append(w[j])
                    test_w.append("".join(w_list))

                print(f"Testing {test_w}")
                res = automaton.test(test_w)
                if false_ex:
                    assert not res
                else:
                    assert res
                print(f"Result: {res}")

    def test_lin_comb_with_pos_inputs(self):
        for i in range(2, 5):
            weights = [ran.randint(-5, 5) for _ in range(i)]
            bias = ran.randint(-5, 5)
            automaton = builder.build_lin_comb_automaton(weights, bias)
            print(f"Testing LinComb with {weights}, bias={bias}")
            for _ in range(1000):
                false_ex = bool(ran.randint(0, 1))
                z_list = []
                z_bin_list = []
                for j in range(i):
                    z = ran.randint(0, 20)
                    z_bin = "0" + bin(int(abs(z))).split('b')[1][::-1]
                    # z_bin = "1" + z_bin if z < 0 else "0" + z_bin
                    z_list.append(z)
                    z_bin_list.append(z_bin)

                to_sum = [weights[j] * z_list[j] for j in range(i)]
                print(to_sum)
                if not false_ex:
                    res = sum(to_sum) + bias

                else:
                    res = sum(to_sum) + bias + ran.randint(1, 1000)
                if res <= 0:
                    res_bin = "0" + bin(int(abs(0))).split('b')[1][::-1]
                    false_ex = False
                else:
                    res_bin = "0" + bin(int(abs(res))).split('b')[1][::-1]
                # res_bin = "1" + res_bin if res < 0 else "0" + res_bin
                z_bin_list.append(res_bin)

                max_len = math.ceil(
                    math.log2(i * max([abs(z) for z in z_list] + [abs(res)] + [abs(z) for z in to_sum])) + 1) + 1
                z_bin_list = [z_bin.ljust(max_len, '0') for z_bin in z_bin_list]

                print(f"sum({z_list}) with weights = {res}")
                print(f"Test {not false_ex} Example")
                test_w = []

                for j in range(max_len):
                    w_list = []
                    for w in z_bin_list:
                        w_list.append(w[j])
                    test_w.append("".join(w_list))

                print(f"Testing {test_w}")
                res = automaton.test(test_w)
                if false_ex:
                    assert not res
                else:
                    assert res
                print(f"Result: {res}")