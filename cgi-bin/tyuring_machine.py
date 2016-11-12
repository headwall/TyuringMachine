import cgi #импортируем модуль с методами обработки форм

form = cgi.FieldStorage() #получаем форму от клиента 

def inputData():
	rows = form.getfirst("program", "empty") #получаем значение поля с именем "program", в котором пользователь ввел матрицу программы
	rows = rows.split("\r\n") #разделяем предыдущее значение на строки

	alphabet = rows[0].split(" ") #получаем из первой строки ввода, алфавит программы
	alphabet = {alphabet[i]:i for i in range(len(alphabet))} #создаем словарь вида {элемент алфавита: его инндекс в массиве}, 
															 #например {"1":0, "2":1, "3":"2"}, если алфавит машины 1, 2, 3
	rowsTemp = rows[1:] #убираем алфавит (находящийся в нулевой строке) из ввода
	rowsTemp = [row.split(" ") for row in rowsTemp] #делим каждую строку во входной матрице на элементы 
													#и получаем таким образом двумерный массив
	matrix = {row[0]: row[1:] for row in rowsTemp} #создаем словарь путем сопоставления состояния, находящегося в нулевом элементе 
													#строки и всех остальных элементов строки, таким образом, 
													#если на текущем шаге матрица имеет вид
													#q1 q01L q31R q12R q30R
													#q2 q02C q22R q10R q21R
													#q3 q00R q22L q32C q12L
													#она будет иметь вид словаря с ключом в виде нулевого символа матрицы и 
													#остальными элементами в качестве значения
													#{'q1': ['q01L', 'q31R', 'q12R', 'q30R'],
													# 'q2': ['q02C', 'q22R', 'q10R', 'q21R'],  
													# 'q3': ['q00R', 'q22L', 'q32C', 'q12L']}

	states = list(matrix.keys()) #здесь будет массив состояний

	tape = form.getfirst("tape", "empty") #получаем значение поля с именем "tape", в котором пользователь ввел ленту
	tape = tape.split(" ") #разделяем предыдущее значение на элементы
	print("tape: {}<br>".format(tape)) #выводим ленту для наглядности
	print("matrix: {}<br>".format(matrix)) #выводим матрицу для наглядности
	return alphabet,states,matrix,tape

def main():
	print("Content-type: text/html\n")
	print("""<!DOCTYPE HTML>
	        <html>
	        <head>
	            <meta charset="utf-8">
	            <title>Tyuring machine</title>
	        </head>
	        <body>""")

	print("<h1>Tyuring machine</h1>")
	alphabet,states,matrix,tape = inputData() #вводим данные
	direction = {"L":-1,"C":0,"R":1} #реализуем словарь и сопоставляем с буквенным значением направления число для движения по слову
	curWord = tape #исполняем условие, что входная лента не меняется в процессе выполнения программы
	curState = "q1" #текущее состояние машины 
	nextState = "" #состояние, в которое перешла машина
	curPos = 1 #текущая позиция в ленте
	step = 1 #счетчик количества шагов
	lentaSize = len(tape) #переменная, хранящая размер ленты
	working = True
	while working:
		if step>200:
			print("Too many iterations")
			break
		if curState == "q0":
			print("Stop")
			break
		try:
			print("<h3>Step: " + str(step) + "</h3>")
			curElement = curWord[curPos]
			if curElement == "s0":
				if curPos == len(curWord)-1:
					curWord = curWord + ["s0"]
				else:
					curWord = ["s0"] + curWord

			col = alphabet[curElement] #выбираем столбец во входной матрице (матрице команд)
			posInMatrix = matrix[curState][col] #выбираем элемент в матрице (команду)
			if posInMatrix == "-":
				print("There is no way")
				break
			else:
				curMatrixValue = posInMatrix[2] #значение, на которое нужно заменить элемент в ленте
				curMatrixDirection = posInMatrix[3] #берем из текущего элемента матрицы команд направление для движения по ленте
				curWord[curPos] = curMatrixValue #заменяем элемент в ленте на нужный
				print("<p>")
				print("Current word: " + str(curWord) + "<br>")

				nextState = posInMatrix[0:2] # берем из из текущего элемента матрицы команд состояние, к торое должна перейти машина
				print("Machine's next state: " + nextState + "<br>")
				curState  = nextState #осуществляем переход в следующее состояние машины

				#curState = nextState

				print("Current position: " + str(curPos) + "<br>")
				curPos += direction[curMatrixDirection] #двигаемся по слову (если "L", то текущая позиция = текущая позиция - 1 и т.п.)
				step += 1 #увеличиваем счетчик шагов
				print("</p>")
		except:
			#если слово не может быть обработано данной программы, выводим сообщение об этом
			print("Program can't handle this word")
			break

	print("""</body>
	        </html>""")

main() #вызов главной функции