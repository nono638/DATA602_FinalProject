def StructureEquality(x,y):
    if type(x) == list:
        x = "".join(x)
    if type(y) == list:
        y = "".join(y)
    x = x.replace("_","")
    y = y.replace("_", "")
    #print("x: {}".format(x))
    #print("y: {}".format(y))
    if x == y:
        return True
    else:
        return False


if __name__ == '__main__':
    print(StructureEquality(['cvc'],'cvc') )
    print()

    print( StructureEquality( ['cvc', '_vc'], 'cvcvc') )
    print()

    print(StructureEquality(['cvc', '_v_'], 'cvcv'))
    print()



