from layout import Layout, csv_vis_type, layout_type, fill_layouts, output_layouts
import argparse

parser = argparse.ArgumentParser(description='Generator naključnih sedežnih redov.')

parser.add_argument('-f', '--filename', dest='students',
                    type=csv_vis_type, required=True, nargs=1, action='store',
                    help='Datoteka s prijavljenimi študenti, skopirana z VISa. Vključuje naslovno vrstico.')

parser.add_argument('-l', '--layout', dest='layouts',
                    type=layout_type, required=True, nargs='+', action='extend',
                    help='Imena razporedov v učilnicah, kjer se piše izpit. Razporedi so na voljo v mapi ucilnice/')

parser.add_argument('-t', '--timeslot', dest='slots',
                    type=str, required=False, nargs='+', action='extend',
                    help='Imena terminov, ki naj jih bo enako kot razporedov.')

parser.add_argument('-s', '--seed', dest='seed', type=int, required=False, nargs=1,
                    help='Seme generatorja naključnih števil.')

parser.add_argument('-o', '--output', dest='output', type=argparse.FileType('w', encoding='utf8'),
                    required=True, nargs=1, help='Pot do izhodne datoteke.')

parser.add_argument('--vpisne', help='Če želite vključiti vpisne številke.', action='store_true')

args = parser.parse_args()
students = args.students[0]
layouts = args.layouts
slots = args.slots
if slots:
    assert len(slots) == len(layouts), "Names must be given for all slots."
    for l, s in zip(layouts, slots):
        l.name = s

num_students = len(students)
capacity = sum(layout.capacity for layout in layouts)
assert capacity >= num_students, \
        "V učilnicah je le %d sedežev, kar ni dovolj za %d študentov." % (capacity, num_students)

fill_layouts(layouts, students, args.seed[0] if args.seed is not None else None)
output_layouts(layouts, args.output[0], args.vpisne)
print("Output saved to '%s'." % args.output[0].name)
