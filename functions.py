import cv2
import numpy as np


def findContour(contour, img):
    min_area = 1000

    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)

    x, y, _, _ = cv2.boundingRect(approx)

    name_contour = None
    color = None

    if (len(approx) == 4 and cv2.contourArea(contour) >= min_area):

        name_contour = "Square"
        color = (0, 0, 255)

    elif (len(approx) == 12 and cv2.contourArea(contour) >= min_area):

        name_contour = "Cross"
        print("ENTREI")
        color = (0, 255, 0)


    elif (len(approx) > 12 and cv2.contourArea(contour) >= min_area):

        name_contour = "Circle"
        color = (255, 0, 0)

    
    if(name_contour in ["Square", "Cross", "Circle"]):
        
        #verifica a existência do objeto com base na quantidade de pixels que possui
        centro_x = None
        centro_y = None 

        M = cv2.moments(contour)
        if M["m00"] != 0:   # Evita divisão por zero
            centro_x = int(M["m10"] / M["m00"])
            centro_y = int(M["m01"] / M["m00"])

        cv2.drawContours(img, [approx], -1, color, 2)
        cv2.putText(img, name_contour, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 127, 255))

        if (centro_x != None) and (centro_y != None):
            cv2.circle(img,(centro_x, centro_y), 5,(0, 127, 255),-1)

    return name_contour



    


'''Função responsável por determinar a forma geométrica com base no contorno já encontrado.'''

def findShapes(contours, img, hierarquia):

    #---------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------#
    # def findContour(contour):
        
    #     min_area = 1000

    #     approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)

    #     x, y, _, _ = cv2.boundingRect(approx)

    #     name_contour = None
    #     color = None

    #     if (len(approx) == 4 and cv2.contourArea(contour) >= min_area):
    #         name_contour = "Square"
    #         color = (0, 0, 255)

    #     elif (len(approx) == 12 and cv2.contourArea(contour) >= min_area):
    #         name_contour = "Cross"
    #         print("ENTREI")
    #         color = (0, 255, 0)

    #     elif (len(approx) > 12 and cv2.contourArea(contour) >= min_area):
    #         name_contour = "Circle"
    #         color = (255, 0, 0)
        
    #     return (name_contour, color)
    #---------------------------------------------------------------------------------#
    #---------------------------------------------------------------------------------#

    for i, contour in enumerate(contours):
        # approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)

        index_parent_contour = hierarquia[0][i][3]

        # #verifica a existência do objeto com base na quantidade de pixels que possui
        # centro_x = None
        # centro_y = None 

        # M = cv2.moments(contour)
        # if M["m00"] != 0:   # Evita divisão por zero
        #     centro_x = int(M["m10"] / M["m00"])
        #     centro_y = int(M["m01"] / M["m00"])

    #---------------------------------------------------------------------------------------------------#
    # index_parent_contour = -1 significa que o atual contorno(contorno de indice i) não está contido dentro de um contorno maior, ou seja, não tem pai
    # index_parent_contour =! -1 significa que o atual contorno(contorno de indice i) está contido dentro de um contorno maior, ou seja, ele tem um pai

        if (index_parent_contour != -1 ): #está verificando se o atual contorno possui um pai e se esse atual contorno é um quadrado
            findContour(contour, img)
            
            #figure = findContour(contours[index_parent_contour],img) #inicialmente assume o papel de contorno pai
            #figure = findContour(contour,img)

            #if(figure[0] == "Square"):
            #     figure = findContour(contour)
                
                # name_contour = figure[0]
                # color = figure[1]
                # x,y = figure[2], figure[3]
                # approx = figure[4]

                # if(name_contour in ["Square", "Cross", "Circle"]):
                    
                #     if(name_contour == "Cross"):
                #         print("CROSS")

                #     cv2.drawContours(img, [approx], -1, color, 2)
                #     cv2.putText(img, name_contour, (x,y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 127, 255))

                #     if (centro_x != None) and (centro_y != None):
                #         cv2.circle(img,(centro_x, centro_y), 5,(0, 127, 255),-1)
        
        #elif(findContour(contour, img) == "Cross"):
            #figure = findContour(contour,img)



'''Função responsável por aplicar operações morfológicas na imagem.'''

def MorphologyOperations(img, slider_value):

    value_matrix = (5,5)
    kernel = np.ones(value_matrix , np.uint8)

    if slider_value != 0:

        #erosão: remove ruídos e pequenas estruturas, reduzindo o tamanho dos objetos brancos na imagem.
        if slider_value == 1:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.erode(img, element_estr, iterations = 2)

        #dilatação: expande as regiões brancas da imagem, preenchendo pequenos buracos.
        elif slider_value == 2:
            element_estr = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, value_matrix)
            img = cv2.dilate(img, element_estr, iterations=2)

        #abertura: realiza erosão seguida de dilatação, útil para remover pequenos ruídos.
        elif slider_value == 3:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.morphologyEx(img, cv2.MORPH_OPEN, element_estr)
        
        #fechamento: realiza dilatação seguida de erosão, útil para fechar buracos em objetos.
        elif slider_value == 4:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, element_estr)

        #gradiente: obtém o contorno dos objetos ao calcular a diferença entre a dilatação e a erosão.
        elif slider_value == 5:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, element_estr)
        
        #top-hat: realça detalhes menores e variações de intensidade na imagem.
        elif slider_value == 6:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, element_estr)
            
        #black-Hat: destaca regiões escuras em fundos claros.
        elif slider_value == 7:
            element_estr = cv2.getStructuringElement(cv2.MORPH_RECT, value_matrix)
            img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, element_estr)


    return img
