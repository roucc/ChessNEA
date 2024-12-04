NEA notes

chess960 possible

documentation
    -need to make it client focused.
    -should be able to give the analysis and design to a programmer
    -should flow logically
    -move sub-objectives to objectives
    -light mode screenshots
    -export code to pdf to put in document (print addition)
    -ongoing testing (challenges during imoplementation)
    -implementation highlights in code


    future improvements:
    -batching,multithreading (GIL C code runs in parallel with python (AI) but breaks top layer alphabetapruning)

code
    -haha enpassant is broken
    -75 move rule fix
    -pypy

problems:
it runs so slowly, do profiling


if black is being checked:
see if black king position is in whites valid moves, if so, is check

video:
-example of it working before
-test number and objective and description before test
-show test and that it satisfies



"fen": "2bq1rk1/pr3ppn/1p2p3/7P/2pP1B1P/2P5/PPQ2PB1/R3R1K1 w - -",
"cp": 311

{(1, 500): {'draw': 0, 'errors': 14, 'me win': 1, 'stockfish win': 9},
 (1, 1000): {'draw': 0, 'errors': 4, 'me win': 0, 'stockfish win': 10},
 (1, 1500): {'draw': 0, 'errors': 11, 'me win': 0, 'stockfish win': 10},
 (1, 2000): {'draw': 0, 'errors': 8, 'me win': 0, 'stockfish win': 10},
 (1, 2500): {'draw': 0, 'errors': 9, 'me win': 0, 'stockfish win': 10},
 (2, 500): {'draw': 2, 'errors': 3, 'me win': 5, 'stockfish win': 3},
 (2, 1000): {'draw': 0, 'errors': 7, 'me win': 7, 'stockfish win': 3},
 (2, 1500): {'draw': 2, 'errors': 12, 'me win': 0, 'stockfish win': 8},
 (2, 2000): {'draw': 2, 'errors': 7, 'me win': 1, 'stockfish win': 7},
 (2, 2500): {'draw': 0, 'errors': 10, 'me win': 1, 'stockfish win': 9},
 (3, 500): {'draw': 1, 'errors': 15, 'me win': 8, 'stockfish win': 1},
 (3, 1000): {'draw': 1, 'errors': 2, 'me win': 5, 'stockfish win': 4},
 (3, 1500): {'draw': 0, 'errors': 10, 'me win': 5, 'stockfish win': 5},
 (3, 2000): {'draw': 2, 'errors': 17, 'me win': 2, 'stockfish win': 6},
 (3, 2500): {'draw': 2, 'errors': 12, 'me win': 0, 'stockfish win': 8}}

elo table difference
https://www.318chess.com/elo.html
 +800	0.99%
+750	1.32%
+700	1.75%
+650	2.32%
+600	3.07%
+550	4.05%
+500	5.32%
+450	6.98%
+400	9.09%
+350	11.77%
+300	15.10%
+250	19.17%
+200	24.03%
+150	29.66%
+100	35.99%
+50	42.85%
0	50.00%
