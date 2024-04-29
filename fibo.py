def main():
    p1 =1
    p2=1
    i = 0
    while i < 20:
        p1,p2 = p2,p1+p2
        print(p1)
        i += 1
if __name__ == '__main__':
    main()