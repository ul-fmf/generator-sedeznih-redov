# Generator sedežnih redov

Orodje, ki za seznam študentov vzet iz VIS-a in izbrane razporede učilnic
zgenerira naključni sedežni red. To počne tako, da prebere "zemljevid" učilnice, kjer ima vsak sedež
prioriteto, in najprej zapolni sedeže s prioriteto 1, nato s prioriteto 2, itd...

Zemljevidi učilnic so podani v mapi `ucilnice` in izgledajo
kot mreže polj, ločenih s presledki, kjer je vsako polje eno izmed naštetega:

 - celo število, ki predstavlja prioriteto (lahko so dvomestne
 - znak `K`, ki predstavlja kateder (za orientacijo)
 - katerikoli drug niz, ki predstavlja neveljaven sedež (nekaj more biti, da se mreža zapolni)

Primer učilnice s katedrom v prvi vrsti in štirimi vrstami sedežev z različno prioriteto:
```
K K X X
1 1 2 2
2 2 1 1
1 1 2 2
2 2 1 1
```

## Tehnične zahteve

Za uporabo potrebujete Python 3.7 ali novejši. Program izpiše `.tex` datoteko,
tako da je za uporaben sedežni red potrebno imeti tudi osnoven prevajalnik `LaTeX`-a.

## Uporaba

Primer uporabe:

```
python generator-sedeznih-redov.py -f demo_studenti.txt -l 310 310 -t "3.10 dopoldne" "3.10 popoldne" -o sedezni_red.tex
```
Izhod programa:
```
Priority 1: 24 / 24 seats filled
Priority 2: 17 / 20 seats filled
Output saved to 'sedezni_red.tex'.
```

Program prebere podatke o študentih iz datoteke `demo_studenti.txt`, podana z zastavico `-f`, ki izgleda kot:
```
Št.	Vpisna št	Priimek	Ime	Status	Način študija	Št.opr.	Sk.opr.	Vpis pred.	Ocena vaj	Opombe
1	28191000  	Aaaaaaaaaaa	Aaaaaaa	 	redni	1	1	2019/20
2	28191000  	Aaaaaaaaaa	Aaaa	 	redni	1	1	2019/20
3	28191000  	Aaaaaaa	Aaaa	 	redni	1	1	2019/20
4	28191000  	Aaaaaaaa	Aaaa	 	redni	1	1	2019/20
5	28191000  	Aaaaaa	Aaaa	 	redni	1	1	2019/20
```

Tako datoteko dobimo, če na VISu pogledamo prijave na izpit in kar v brskalniku označimo celo tabelo
in jo skopiramo v `.txt` datoteko. Formalno je to `.csv` datoteka s separatorjem `\t`.

Z zastavico `-l` dodamo zemljevide vseh učilnic, ki jih bomo uporabljali. Podamo samo ime datoteke z
zemljevidom, ki jo program išče v mapi `ucilnice/` s končnico `.txt`. Za ime `VFP` program prebere
zemljevid `ucilnice/VFP.txt`. S spremembo zemljevida lahko prioritete sedežev nastavite po svojih
željah.

Z zastavico `-t` lahko opcijsko poimenujemo vsak termin/skupino, sicer jih program poimenuje sam.

Z zastavico `-o` podamo pot do izhodne `.tex` datoteke, kjer so tabele s sedežnimi redi.

Sedežni red privzeto vsebuje samo imena in priimke.
Vpisne številke lahko dodamo z zastavico `--vpisne`.

Z zastavico `-s` lahko nastavimo seme generatorja, da vedno dobimo enako zmešan razpored.

Za dodatno pomoč lahko uporabimo `-h` ali `--help`.

Jure Slak
