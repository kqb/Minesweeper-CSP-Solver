from tkinter import *


class FieldButton(Button):
    '''FieldButton Class:
       This is a class extend Button.
    '''

    def __init__(self, x, y, frame, images, value=0):

        self.img_blank = images['blank']
        self.img_mine = images['mine']
        self.img_hit_mine = images['hit_mine']
        self.img_flag = images['flag']
        self.img_wrong = images['wrong']
        self.img_no = images['no']

        super(FieldButton, self).__init__(frame,image = self.img_blank)

        self._x = x
        self._y = y
        self._value = value
        self.is_a_mine = False
        self.is_visible = False
        self.is_flagged = False
        if value == -1:
            self.is_a_mine = True

    @property
    def x(self):
        '''Return coordinate x.

        :return: int
        '''

        return self._x

    @property
    def y(self):
        '''Return coordinate y.

        :return: int
        '''

        return self._y

    @property
    def value(self):
        '''Return button value. -1 indicates mine and 0-8 indicate the amount of mines in surrounding buttons.

        :return: int
        '''

        return self._value

    @value.setter
    def value(self, value):
        '''Set button value. -1 indicates mine and 0-8 indicate the amount of mines in surrounding buttons.
        '''

        self._value = value
        if self._value == -1:
            self.is_a_mine = True

    def flag(self):
        '''Flag button if it's not flagged and not showed; unflag it otherwise.
        '''

        if not self.is_visible:
            if self.is_flagged:
                self.config(image = self.img_blank)
            else:
                self.config(image = self.img_flag)
            self.is_flagged = not self.is_flagged


    def is_flag(self):
        '''Return True if button is flagged; False otherwise.

        :return: bool
        '''

        return self.is_flagged

    def place_mine(self):
        '''Set button to a mine if it's not a mine. Return True if set button sucessfully; False otherwise.

        :return: bool
        '''

        if not self.is_a_mine:
            self._value = -1
            self.is_a_mine = True
            return True
        return False

    def is_mine(self):
        '''Return true if button it's a mine; false otherwise;

        :return: bool
        '''

        return self.is_a_mine

    def show(self):
        '''Set button to visible if it's not flagged.
        '''

        if not self.is_visible and not self.is_flagged:
            self.is_visible = True
            if self.is_mine():
                self.config(image = self.img_mine)
            else:
                self.config(image = self.img_no[self._value])

    def is_show(self):
        '''Return True if button is visible; False otherwise.
        '''

        return self.is_visible

    def reset(self):
        '''Reset button to empty button.
        '''

        self._value = 0
        self.is_a_mine = False
        self.is_visible = False
        self.is_flagged = False
        self.show_blank()

    def show_wrong_flag(self):
        '''Set button to wrong flag.
        '''

        self.config(image = self.img_wrong)

    def show_hit_mine(self):
        '''Set button to hit mine.
        '''

        self.config(image = self.img_hit_mine)

    def show_blank(self):
        '''Set button to blank.
        '''

        self.config(image = self.img_blank)


