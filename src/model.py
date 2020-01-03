class Model:
    
    def __init__(self, betLeadTru, betNoLeadTru, betLeadNoTru, betNoLeadNoTru, offs, add, pos, recip):
        self.betLeadTru=betLeadTru #Min rank to count card in bet if leading and the card is Trump
        self.betNoLeadTru=betNoLeadTru #Min rank to count card in bet if not leading but card is Trump
        self.betLeadNoTru=betLeadNoTru #Min rank to count card in bet if leading but card isn't Trump
        self.betNoLeadNoTru=betNoLeadNoTru #Min rank to count card in bet if not leading and card isn't Trump
        self.offs=offs #Base offset number, varies by number of cards dealt
        self.add=add #Will the model determine offset using addition/subtraction or multiplication/division
        self.pos=pos #Will the model use addition or multiplication instead of subtraction or division
        self.recip=recip #Will the model use reciprocal subtraction or division

    def offset(self, num):
        if self.pos and self.add:
            return self.offs+num
        if self.pos and not self.add:
            return self.offs*num
        if not self.pos and self.add:
            return self.offs-num if self.recip else num-self.offs
        if not self.pos and not self.add:
            try:
                return self.offs/num if self.recip else num/self.offs
            except: #Division of 0
                return 0