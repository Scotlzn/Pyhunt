import pygame

# 1 = Wave Text
# 2 = Shop Text
# 3 = UI Text
order = {
	1: ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9'],
	2: ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0',':'],
	3: ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9',':','-']
}

class Text():
	def __init__(self, path, spacing, type):
		self.spacing = spacing
		self.character_order = order[type]
		font_img = pygame.image.load(path).convert()
		current_char_width = 0
		between_char = False
		self.characters = {}
		character_count = 0
		for x in range(font_img.get_width()):
			c = font_img.get_at((x, 0))
			if c[0] == 127:
				if not between_char:
					char_img = self.clip(font_img, x-current_char_width, 0, current_char_width, font_img.get_height())
					self.characters[self.character_order[character_count]] = char_img
					character_count += 1
					current_char_width = 0
					between_char = True
			else:
				current_char_width += 1
				between_char = False
		self.space_width = self.characters[self.character_order[0]].get_width()

	def clip(self, surf, x, y, width, height):
		handle = surf.copy()
		clipR = pygame.Rect(x,y,width,height)
		handle.set_clip(clipR)
		image = surf.subsurface(handle.get_clip())
		return image.copy()	

	def render(self, surf, text, loc):
		x_offset = 0
		for char in text:
			if char != ' ':
				self.characters[char].set_colorkey((0,0,0))
				surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
				x_offset += self.characters[char].get_width() + self.spacing
			else:
				x_offset += self.space_width + self.spacing