#This is the main loop. It calls all the required

#global packages

#my packages
import logics as lg


def main():
    lg.generate_layup

    lg.partitions

    process geometry

    assign materials

    place components

    define solver

    define interaction

    define load

    pass


if __name__ == '__main__':
    main()