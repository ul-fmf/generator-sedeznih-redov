from collections import defaultdict
import random
from typing import List, Dict, Tuple, Set, Union
from dataclasses import dataclass
import csv


@dataclass
class Student:
    ime: str
    priimek: str
    vpisna_stevilka: str


def csv_vis_type(filename):
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter='\t')
        prijavljeni = []
        for row in reader:
            prijavljeni.append(Student(
                ime=row['Ime'].strip(),
                priimek=row['Priimek'].strip(),
                vpisna_stevilka=row['Vpisna št'].strip()
            ))
        return prijavljeni


class Layout:
    def __init__(self, name, rows, cols, layout):
        self.name: str = name
        self.rows: int = rows
        self.cols: int = cols
        self.layout: List[List[str]] = layout
        self.students: List[List[Union[None, Student]]] = [[None]*self.cols for _ in range(self.rows)]

        self.capacity: int = 0
        self.seats_by_priority: Dict[int, Set[Tuple[int, int]]] = defaultdict(set)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.layout[i][j].isdecimal():
                    priority = int(self.layout[i][j])
                    self.capacity += 1
                    self.seats_by_priority[priority].add((i, j))

    def __str__(self):
        return "\n".join(" ".join(map(str, row)) for row in self.layout)

    __repr__ = __str__

    @staticmethod
    def load(filename):
        with open(filename) as f:
            file = [line.split() for line in f]
            assert len(file) > 0, "File must not be empty"
            assert all(len(line) == len(file[0]) for line in file), "All line must have the same length"
            return Layout(filename, len(file), len(file[0]), file)

    def priority_counts(self):
        """Returns dict counting how many seats of which priority we have."""
        return {p: len(seats) for p, seats in self.seats_by_priority.items()}

    def fill(self, i: int, j: int, student: Student):
        priority = int(self.layout[i][j])
        self.students[i][j] = student
        self.seats_by_priority[priority].remove((i, j))

    def tex(self, public):
        def show(i, j, s):
            if s is None:
                if self.layout[i][j] == 'K':
                    return '(kateder)'
                if self.layout[i][j] == 'H':
                    return '(prehod)'
                if self.layout[i][j] == 'Z':
                    return '(prazno)'  # Nedovoljeni sedeži zaradi korone
                if not self.layout[i][j].isdecimal():
                    return '(prazno)'
                return '(prosto)'
            if public:
                return r"%s" % s.vpisna_stevilka
            else:
                return r" %s \newline %s \newline %s" % (s.ime, s.priimek, s.vpisna_stevilka)

        strut = r'\rule[-1.5cm]{0pt}{2.4cm} & '

        contents = [r'\section*{%s} \vspace{1cm}' % self.name,
                    r'\begin{tabularx}{\columnwidth}{c|%s} \cline{2-%d}' % ('X|' * self.cols, self.cols + 1)]
        for row in range(self.rows):
            contents.append(strut + ' & '.join(show(row, i, s) for i, s in enumerate(self.students[row])) + r'\\ \cline{2-%d}' % (self.cols+1))
        contents.append(r'\end{tabularx}')
        return '\n'.join(contents)

    def student_list(self):
        return [self.students[i][j]
                for i in range(self.rows) for j in range(self.cols) if self.students[i][j]]


def layout_type(layout):
    return Layout.load(f"ucilnice/{layout}.txt")


def fill_layouts(layouts, students, seed=None):
    """Fill seats by increasing priority. First priority 0, for each classroom, then priority 1..."""
    if seed is not None:
        random.seed(seed)
    random.shuffle(students)
    student_index = 0

    student_per_priority = defaultdict(int)
    seats_per_priority = defaultdict(int)
    priorities = sorted({p for layout in layouts for p in layout.priority_counts().keys()})
    for p in priorities:
        for layout in layouts:
            seats = list(layout.seats_by_priority[p])
            seats_per_priority[p] += len(seats)
            random.shuffle(seats)
            for seat in seats:
                if student_index == len(students):
                    continue
                layout.fill(seat[0], seat[1], students[student_index])
                student_index += 1
                student_per_priority[p] += 1

    for p in seats_per_priority:
        print("Priority %d: %d / %d seats filled" % (p, student_per_priority[p], seats_per_priority[p]))


def output_layouts(layouts, output_file, public):
    header = r"""
\documentclass[a4paper,oneside,12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{tabularx}
\usepackage[none]{hyphenat}
\usepackage[
  top=2.5cm,
  bottom=2.5cm,
  left=1.2cm,
  right=1.4cm
]{geometry}
\usepackage{multicol}

\pagestyle{empty}

\begin{document}
\centering
"""
    footer = """
\end{document}
"""
    contents = [layout.tex(public) for layout in layouts]
    if public:
        # print number: slot mapping
        slots = {student.vpisna_stevilka: layout.name
                 for layout in layouts for student in layout.student_list()}

        tex_list = [r'\section*{Razporeditev po učilnicah}\begin{multicols}{2}\begin{tabbing}',
                    r'\hspace{2cm} \= \hspace{3cm} \kill']
        for v, s in sorted(slots.items()):
            tex_list.append(r'  %s \> %s \\' % (v, s))
        tex_list.append(r'\end{tabbing}\end{multicols}\newpage')

        contents = ['\n'.join(tex_list)] + contents

    output_file.write(header + '\n \\newpage \n'.join(contents) + footer)
