from encapsulation import DL_Process, Print_Welcome


def konachan_main():
    Print_Welcome().konachan()
    while True:
        choice = input('select operation: ')
        if choice == '1':
            DL_Process().bulk_dl()
        elif choice == '2':
            DL_Process().chk_dl()
        elif choice == '3':
            exit()
        else:
            print('Invalid Input')


if __name__ == '__main__':
    konachan_main()
