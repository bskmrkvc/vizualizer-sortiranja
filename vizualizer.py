from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PyQt5.uic import loadUi
from PyQt5 import QtTest
from random import sample, choices
from sys import argv, exit

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        loadUi("interfejs.ui", self)
        self.c_height = 421
        self.font = QFont()
        self.font.setPointSize(12)
        self.speed = {
            0: ["0.25x", 3],
            1: ["0.5x", 2],
            2: ["0.75x", 1.5],
            3: ["1x", 1],
            4: ["1.25x", 0.5],
            5: ["1.5x", 0.2],
            6: ["1.75x", 0.1],
        }
        self.colors = {
            "red": QColor(243, 23, 23),
            "green": QColor(1, 169, 8),
            "blue": QColor(0, 0, 250),
            "black": QColor(0, 0, 0),
            "violet": QColor(166, 0, 218),
            "orange": QColor(255, 146, 0),
        }
        self.sorts_desc = {
            "Bubble Sort": ["O(n²)", "O(1)"],
            "Insertion Sort": ["O(n²)", "O(1)"],
            "Selection Sort": ["O(n²)", "O(1)"],
            "Quick Sort": ["O(nlogn)", "O(nlogn)"],
            "Merge Sort": ["O(nlogn)", "O(n)"],
        }
        self.pen = QPen(self.colors["black"], 3)
        self.generate.clicked.connect(self.generateArray)
        self.lenslider.valueChanged.connect(self.updatelength)
        self.minslider.valueChanged.connect(self.updatemin)
        self.maxslider.valueChanged.connect(self.updatemax)
        self.speedslider.valueChanged.connect(self.updatespeed)
        self.start.clicked.connect(self.startalgorithm)
        self.show()

    def updatelength(self):
        self.len = self.lenslider.value()
        self.lenval.setText(str(self.len))

    def updatemin(self):
        self.mn = self.minslider.value()
        self.minval.setText(str(self.mn))

    def updatemax(self):
        self.mx = self.maxslider.value()
        self.maxval.setText(str(self.mx))

    def updatespeed(self):
        self.sd = self.speedslider.value()
        self.speedval.setText(self.speed[self.sd][0])


    # Kreiranje nasumicnog niza
    def generateArray(self):
        self.start.setDisabled(False)
        self.tmcomp.setText("")
        self.spcomp.setText("")
        self.len = self.lenslider.value()
        self.mn = self.minslider.value()
        self.mx = self.maxslider.value()
        if (self.mx - self.mn + 1) >= self.len:
            self.arr = sample(range(self.mn, self.mx + 1), self.len)
        else:
            self.arr = choices(range(self.mn, self.mx + 1), k=self.len)

        self.drawData(["red"] * (self.len))

    # Crtanje pravougaonika na ekranu
    def drawData(self, color):
        self.scene = QGraphicsScene()
        self.c_width = 831 - 13 * self.len
        x_width = self.c_width / (self.len + 1)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        maxele = max(self.arr)
        normalizedData = [i / maxele for i in self.arr]
        for i, height in enumerate(normalizedData):
            x0 = i * (x_width + 13)
            y0 = self.c_height - height * 370
            x1 = x_width
            y1 = self.c_height - y0
            self.brush = QBrush(self.colors[color[i]])
            self.scene.addRect(x0, y0, x1, y1, self.pen, self.brush)
            num = self.scene.addText(str(self.arr[i]))
            num.setPos(x0, y0 - 30)
            num.setFont(self.font)

    # Logika koja se izvrsava nakon pritiska na start dugme
    def startalgorithm(self):
        self.generate.setDisabled(True)
        self.start.setDisabled(True)
        self.selected_algo = self.algorithm.currentText()
        self.sd = self.speed[self.speedslider.value()][1]
        if self.selected_algo == "Bubble Sort":
            self.BubbleSort(self.len, self.arr, self.drawData)
        elif self.selected_algo == "Insertion Sort":
            self.InsertionSort(self.len, self.arr, self.drawData)
        elif self.selected_algo == "Selection Sort":
            self.SelectionSort(self.len, self.arr, self.drawData)
        elif self.selected_algo == "Merge Sort":
            self.MergeSort(self.len, 0, self.len - 1, self.arr, self.drawData)
        elif self.selected_algo == "Quick Sort":
            self.QuickSort(self.len, 0, self.len - 1, self.arr, self.drawData)

        self.generate.setDisabled(False)
        self.tmcomp.setText(self.sorts_desc[self.selected_algo][0])
        self.spcomp.setText(self.sorts_desc[self.selected_algo][1])

    # Bubble Sort Algoritam
    def BubbleSort(self,n, arr, drawData):
        for i in range(n - 1):
            for j in range(n - 1 - i):
                drawData([
                    "blue" if x == j or x == j + 1 else "red" for x in range(n - i)
                ] + ["green"] * (i + 1))

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                drawData(["red" for x in range(n - i)] + ["green"] * (i + 1))

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1]  * 1000)

        drawData(["green"] * n)
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000) 

    # Insertion Sort Algoritam
    def InsertionSort(self,n, arr, drawData):
        for i in range(1, n):
            j = i - 1
            x = arr[i]
            drawData(["green"] * j +
                    ["blue" if k == j or k == i else "red" for k in range(j, n)])

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
            while j >= 0 and arr[j] > x:
                arr[j + 1] = arr[j]
                drawData(
                    ["green"] * j +
                    ["blue" if k == j or k == i else "red" for k in range(j, n)])

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                j = j - 1
            arr[j + 1] = x
            drawData(["green"] * i + ["red" for k in range(i, n)])

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
        drawData(["green"] * n)
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)


    # Selection Sort Algoritam
    def SelectionSort(self,n, arr, drawData):
        for i in range(n - 1):
            k = i
            for j in range(i + 1, n):
                L = []
                for x in range(n):
                    if x < i:
                        L.append("green")
                    elif x == i:
                        L.append("violet")
                    elif x == j:
                        L.append("blue")
                    else:
                        L.append("red")
                drawData(L)

                QtTest.QTest.qWait( self.speed[self.speedslider.value()][1]* 1000)
                if arr[j] < arr[k]:
                    k = j
            L = []
            for x in range(n):
                if x < i:
                    L.append("green")
                elif x == k:
                    L.append("orange")
                else:
                    L.append("red")
            drawData(L)

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
            arr[i], arr[k] = arr[k], arr[i]
        drawData(["green"] * n)


    # Merge Sort algoritam
    def MergeSort(self,n, l, h, arr, drawData):
        drawData(["orange" if x in range(l, h + 1) else "red" for x in range(n)])
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
        if l < h:
            mid = (l + h) // 2
            self.MergeSort(n, l, mid, arr, drawData)
            self.MergeSort(n, mid + 1, h, arr, drawData)
            self.Merge(n, l, mid, h, arr, drawData)

        drawData(["green"] * n)


    # Spajanje 2 niza
    def Merge(self,n, l, mid, h, arr, drawData):
        drawData(["orange" if x in range(l, h + 1) else "red" for x in range(n)])
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
        n1 = mid - l + 1
        n2 = h - mid

        # pravljenje 2 privremena niza
        L = [0] * (n1)
        R = [0] * (n2)

        for i in range(0, n1):
            L[i] = arr[l + i]

        for j in range(0, n2):
            R[j] = arr[mid + 1 + j]

        i, j, k = 0, 0, l

        while i < n1 and j < n2:
            S = ["red"] * n
            for x in range(n):
                if x == i + l:
                    S[i + l] = "violet"
                elif x == j + (mid + 1):
                    S[j + (mid + 1)] = "blue"
            drawData(S)

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
            if L[i] <= R[j]:
                arr[k] = L[i]
                drawData(["red" for x in range(n)])

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                i += 1
            else:
                arr[k] = R[j]
                drawData(["red" for x in range(n)])

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                j += 1
            k += 1

        while i < n1:
            arr[k] = L[i]
            drawData(["red" for x in range(n)])

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
            i += 1
            k += 1

        while j < n2:
            arr[k] = R[j]
            drawData(["red" for x in range(n)])

            QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
            j += 1
            k += 1

        drawData(["green" if x in range(l, h + 1) else "red" for x in range(n)])
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)


    # Quick Sort Algoritam
    def QuickSort(self,n, l, h, arr, drawData):
        if l < h:
            p = self.Partition(l, h, arr, drawData)
            self.QuickSort(n, l, p - 1, arr, drawData)
            self.QuickSort(n, p + 1, h, arr, drawData)
        drawData(["green"] * n)

   
    def Partition(self,l, h, arr, drawData):
        pivot_index = l
        pivot = arr[pivot_index]
        drawData(
            ["violet" if x == pivot_index else "red" for x in range(len(arr))])
        while l < h:
            while l < len(arr) and arr[l] <= pivot:
                R = []
                for x in range(len(arr)):
                    if x == pivot_index:
                        R.append("violet")
                    elif x == l:
                        R.append("blue")
                    else:
                        R.append("red")
                drawData(R)

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                l += 1

            while arr[h] > pivot:
                R = []
                for x in range(len(arr)):
                    if x == pivot_index:
                        R.append("violet")
                    elif x == h:
                        R.append("blue")
                    else:
                        R.append("red")
                drawData(R)

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                h -= 1

            if l < h:
                drawData([
                    "blue" if x == h or x == l else "red" for x in range(len(arr))
                ])

                QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
                arr[l], arr[h] = arr[h], arr[l]
        drawData([
            "blue" if x == h or x == pivot_index else "red"
            for x in range(len(arr))
        ])
        QtTest.QTest.qWait(self.speed[self.speedslider.value()][1] * 1000)
        arr[h], arr[pivot_index] = arr[pivot_index], arr[h]
        return h


app = QApplication(argv)
mainwindow = MainWindow()
exit(app.exec_())
