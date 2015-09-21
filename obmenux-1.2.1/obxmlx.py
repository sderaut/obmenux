
'''obxmlx.py component of
   Openbox Menu Editor X 1.2.1  2015 by SDE

   based on
   Openbox Menu Editor 1.0 beta 
   Copyright 2005 Manuel Colmenero 

     This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.
 
     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.
 
     You should have received a copy of the GNU General Public License
     along with this program; if not, write to the Free Software
     Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


  ObMenux can be used as a module in python scripts, for example, to
  Generate dynamic menus (pipemenus)
'''

import xml.dom.minidom

class ObMenux:
	
	# Internal functions =============================================
	# (These mess with the xml tree)

	def _get_dom_menu(self, menu, parent=None):
		''' given its ID, and its parent (or None for top-level)
		    returns the dom tree of the menu. Recursively. '''
		if menu is None: #BUGFIX was `if not menu` but menu may be falsy and valid
			return self.dom.documentElement #BUGFIX was `return None`
		if parent is None: #BUGFIX was `if not parent` but parent may be falsy
			parent = self.dom.documentElement
		
		for item in parent.childNodes:
			if item.nodeName == "menu" and item.hasChildNodes():
				if item.attributes["id"].nodeValue == menu: return item
				else:
					b = self._get_dom_menu(menu, item)
					if b: return b

	def _get_dom_ref(self, menu, parent):
		''' given its ID, and its parent (or None for top-level)
		    returns the dom tree of the menu. Recursively. '''		
		if parent is None: #BUGFIX was `if not parent` but parent id may be falsy
			parent = self.dom.documentElement
		for item in parent.childNodes:
			if item.nodeName == "menu":
				if not item.hasChildNodes():
					if item.attributes["id"].nodeValue == menu: return item
				else:
					b = self._get_dom_menu(menu, item)
					if b: return b
	
	def _get_dom_item(self,menu,num):
		''' Get an item of 'menu', given its number (order) '''
		if menu is None: #BUGFIX was `if not menu`
			item = self.dom.documentElement
		else:
			item = self._get_dom_menu(menu)
			if not item:
				item = self.dom.documentElement #BUGFIX was `return None`
		i = 0
		for it in item.childNodes:
			if it.nodeType == 1:
				if i == num: return it
				i += 1
	
	def _put_dom_item(self, menu, nodo, pos=None):
		''' Insert a node in the xml tree '''
		parent = self._get_dom_menu(menu)
		if not parent: parent = self.dom.documentElement
		
		if pos == None or pos > self._get_menu_len(menu):
			parent.appendChild(nodo)
		elif pos >= 0:
			ant = self._get_dom_item(menu, pos)
			parent.insertBefore(nodo, ant)
	
	def _get_menu_len(self,menu):
		'''	Get the number of items of a menu '''
		if menu is not None: #BUGFIX was `if menu`
			item = self._get_dom_menu(menu)
			if item is None:
				item = self.dom.documentElement #BUGFIX maybe
		else:
			item = self.dom.documentElement
		i = 0
		if item is None: return i #BUGFIX None has no childNodes
		for it in item.childNodes:
			if it.nodeType == 1:
				i += 1
		return i
	
	def _get_real_num(self,menu,num):
		''' Get "real" item number (counting comments, text, etc. in the XML)
		    Returns None when not 0-based index num not found '''
		if menu is not None: #BUGFIX was `if menu`
			item = self._get_dom_menu(menu)
			if item is None: item = self.dom.documentElement #BUGFIX maybe
		else:
			item = self.dom.documentElement
		i = 0
		n = 0
		for it in item.childNodes:
			if it.nodeType == 1:
				if i == num: return n
				i += 1
			n += 1
	
	def _get_item_props(self,node):
		''' get the properties of an item from the xml, and returns them as a
		    dictionary. '''
		etiqueta = node.attributes["label"].nodeValue
		accion = ""
		param = ""
		for it in node.childNodes:
			if it.nodeType == 1:
				accion = it.attributes["name"].nodeValue
				if accion.lower() == "execute":
					for itm in it.childNodes:
						if itm.nodeType == 1 and (itm.nodeName == "command"
						                       or itm.nodeName == "execute"):
							for item in itm.childNodes:
								if item.nodeType == 3:
									param = item.nodeValue.strip()
									break # first found text is the one to use
							break # use first found command or execute tag
		return { "type": "item", "label": etiqueta, "action": accion,
		         "execute": param }
	
	def _get_menu_props(self, node):
		'''	get the properties of a menu from the xml, and returns them as a
		    dictionary. '''
		lb = ""
		ex = ""
		act = ""
		mid = node.attributes["id"].nodeValue
		if node.hasAttribute("label"):
			lb = node.attributes["label"].nodeValue
		else:
			mnu = self._get_dom_menu(mid)
			if mnu: lb = mnu.attributes["label"].nodeValue
			else: lb = mid
		if not node.hasChildNodes():
			if node.hasAttribute("execute"):
				ex = node.attributes["execute"].nodeValue
				act = "Pipemenu"
			else:
				act = "Link"
		if node.hasAttribute("execute"): ex = node.attributes["execute"].nodeValue
		return { "type": "menu", "label": lb, "action": act, "execute": ex, "id": mid }

	def _get_sep_props(self,node):
		''' get the properties of a separator from the xml, and returns them as
		    a dictionary. '''
		if node.hasAttribute("label"):
			return { "type": "separator",
			         "label": node.attributes["label"].nodeValue }
		else:
			return { "type": "separator" }

	# Public functions ===================================================
	# Most of them are self-explanatory
				
	def loadMenu(self, filename):
		''' opens and closes filename (may throw IO and XML exceptions)
		    sets a model of the XML it contains for this class to edit '''
		fil = open(filename)
		self.dom = xml.dom.minidom.parseString(fil.read())
		fil.close()
	
	def newMenu(self):
		''' sets the current model to an empty Openbox menu '''
		self.dom = xml.dom.minidom.parseString(
		"<?xml version=\"1.0\" ?><openbox_menu></openbox_menu>")
		#self.dom._set_async(False)

	def newPipe(self):
		''' sets the current model to an empty Openbox pipe menu '''
		self.dom = xml.dom.minidom.parseString(
		"<?xml version=\"1.0\" ?><openbox_pipe_menu></openbox_pipe_menu>")
	
	def saveMenu(self, filename):
		''' saves the current model as XML (may throw IO exceptions) '''
		output = open(filename, "w")
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				output.write("%s\n" %(line))
		output.close()
	
	def printXml(self):
		''' prints the current model to stdout as XML '''
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				print(line)
	
	def getXml(self):
		''' returns a string containing XML formed from the current model '''
		res = ""
		for line in self.dom.toprettyxml("\t","\n","utf-8").splitlines():
			if line.strip() != "":
				res = res + "%s\n" % (line)
		return res
				
	def removeItem(self,menu, num):
		''' removes from menu (by ID) item num (0-based index) '''
		if menu is not None: #BUGFIX was `if menu`, bad b/c menuid "" may be falsy
			dom_mnu = self._get_dom_menu(menu)
			if dom_mnu is None:
				dom_mnu = self.dom.documentElement #BUGFIX maybe
		else:
			dom_mnu = self.dom.documentElement
		item = self._get_dom_item(menu,num)
		if item is None:
			# print("Warning: an item was not removed")
			return #BUGFIX let's not destroy the dom
		dom_mnu.removeChild(item)
		item.unlink()
	
	def removeMenu(self,menu):
		''' removes menu (by ID) '''
		dom_mnu = self._get_dom_menu(menu)
		if dom_mnu is None:
			# print("Warning: a menu was not removed")
			return #BUGFIX None has no parentNode
		if not dom_mnu.parentNode:
			self.dom.documentElement.removeChild(dom_mnu)
		else:
			dom_mnu.parentNode.removeChild(dom_mnu)
		dom_mnu.unlink()
	
	def createSep(self, menu, pos=None, label=None):
		''' creates a Separator element in menu (by ID) at pos (0-based index) '''		
		nodo = self.dom.createElement("separator")
		if label is not None:
			nodo.setAttribute("label", label)
		self._put_dom_item(menu, nodo, pos)
			
	def createItem(self, menu, label, action, execute, pos=None):
		''' Creates an item tag in menu (by ID) at pos (0-based index).
		    String label is assigned to the label attribute of the item tag.
		    An action tag is inserted and its name is set to "Execute".
		    The action argument is ignored.
		    String execute is inserted into a command tag. (Literal execute tags
		    are deprecated, though still recognized by obmenux.) '''
		nodo = self.dom.createElement("item")
		nodo.attributes["label"] = label
		accion = self.dom.createElement("action")
		accion.attributes["name"] = "Execute"
		exe = self.dom.createElement("command")
		txt = self.dom.createTextNode("")
		txt.nodeValue = execute
		exe.appendChild(txt)
		accion.appendChild(exe)
		nodo.appendChild(accion)
		self._put_dom_item(menu, nodo, pos)
	
	def createLink(self, menu, mid, pos=None):
		''' at menu and pos
		    creates a menu item that has a menu ID string mid '''
		nodo = self.dom.createElement("menu")
		nodo.attributes["id"] = mid
		self._put_dom_item(menu, nodo, pos)

	def createPipe(self, menu, mid, label, execute, pos=None):
		''' at menu and pos (or append if pos=None)
		    creates a menu item that has the specified id, label, and execute
		    attributes, and no child nodes '''
		nodo = self.dom.createElement("menu")
		nodo.attributes["id"] = mid
		nodo.attributes["label"] = label
		nodo.attributes["execute"] = execute
		
		self._put_dom_item(menu, nodo, pos)
		
	def createMenu(self, menu, label, mid, pos=None):
		''' at menu (by ID) and pos (DOM int)
		    creates a menu that has the specified label and id as attributes,
		    and one empty string for a child node '''
		nodo = self.dom.createElement("menu")
		nodo.attributes["label"] = label
		nodo.attributes["id"] = mid
		txt = self.dom.createTextNode("")
		txt.nodeValue = "\n"
		nodo.appendChild(txt)
		self._put_dom_item(menu, nodo, pos)
		
	def interchange(self, menu, n1, n2):
		''' within menu (by ID) swaps nodes n1 and n2
		    where n1 and n2 are integers representing tags in the menu
		    by a 0-based count (not all DOM nodes in the menu)
		    True when successful '''
		if menu is None:
			dom_mnu = self.dom.documentElement
		else:
			dom_mnu = self._get_dom_menu(menu)
			if dom_mnu is None:
				dom_mnu = self.dom.documentElement
		i1 = self._get_real_num(menu, n1)
		i2 = self._get_real_num(menu, n2)
		if i1 is None or i2 is None:
			return False
		tmp1 = dom_mnu.childNodes[i1].cloneNode(deep=True)
		tmp2 = dom_mnu.childNodes[i2].cloneNode(deep=True)
		dom_mnu.replaceChild(tmp2, dom_mnu.childNodes[i1])
		dom_mnu.replaceChild(tmp1, dom_mnu.childNodes[i2])
		return True
			
	def jumpMove(self, src_menu, n1, dest_menu, n2): # new feature
		''' moves item or menu from source menu n1
		    to before destination menu n2
		    where n1 and n2 are integers representing tags in the menu
		    by a 0-based count before moving the item or menu,
		    (appends when n2 > 0-based count of tags in destination)
		    True when successful '''
		if src_menu is None:
			dom_mnu1 = self.dom.documentElement
		else:
			dom_mnu1 = self._get_dom_menu(src_menu)
			if dom_mnu1 is None:
				dom_mnu1 = self.dom.documentElement
		if dest_menu is None:
			dom_mnu2 = self.dom.documentElement
		else:
			dom_mnu2 = self._get_dom_menu(dest_menu)
			if dom_mnu2 is None:
				dom_mnu2 = self.dom.documentElement
		i1 = self._get_real_num(src_menu, n1)
		if i1 is None:
			return False
		tmp = dom_mnu1.childNodes[i1].cloneNode(deep=True)
		dum = dom_mnu1.removeChild(dom_mnu1.childNodes[i1])
		dum.unlink() # should be unlinked if not used according to docs
		if src_menu == dest_menu and n1 < n2:
		    n2 -= 1
		i2 = self._get_real_num(dest_menu, n2)
		if i2 is None:
			dom_mnu2.insertBefore(tmp, None)
		else:
			dom_mnu2.insertBefore(tmp, dom_mnu2.childNodes[i2])
		return True

	def setItemProps(self, menu, n, label, action, exe):
		''' at position n (0-based DOM count) of menu (by ID)
		    sets the string label attribute and string action name, and
		    when action name is "Execute",
		        sets the item to have at least one command or execute tag
		        containing string exe (preferring command, as execute tag is
		        deprecated, and preferring the first matching tag found)
		    when action is anything else,
		        removes all command or execute tags from the item '''
		itm = self._get_dom_item(menu,n)
		itm.attributes["label"].nodeValue = label
		for it in itm.childNodes:
			if it.nodeType == 1:
				it.attributes["name"].nodeValue = action
				if action.lower() == "execute": # action may be "[E|e]xecute"
					exe_used = False
					if it.childNodes is not None:
						for i in it.childNodes:
							if i.nodeType == 1 and (i.nodeName == "execute" or
							                        i.nodeName == "command"):
								for item in i.childNodes:
									if item.nodeType == 3:
										item.nodeValue = exe
										exe_used = True
										break
								if not exe_used:
									txt = xml.dom.mindom.Text()
									txt.nodeValue = exe
									exe_used = True
									i.appendChild(txt)
								break
					if not exe_used:
						elm = xml.dom.minidom.Element("command")
						txt = xml.dom.minidom.Text()
						txt.nodeValue = exe
						exe_used = True
						elm.appendChild(txt)
						it.appendChild(elm)
				else:
					for item in it.childNodes:
						if item.nodeType == 1 and (item.nodeName == "execute" or
						                           item.nodeName == "command"):
							it.removeChild(item)
							item.unlink()
	
	def setMenuLabel(self, menu, label):
		''' sets the label attribute of menu (by ID) to string label '''
		mnu = self._get_dom_menu(menu)
		if mnu: mnu.attributes["label"].nodeValue = label
	
	def getMenuLabel(self,menu):
		''' returns the string label attribute of menu (by ID)
		    or None if top level '''
		mnu = self._get_dom_menu(menu)
		if mnu: return mnu.attributes["label"].nodeValue

	def setRefLabel(self, parent, mid, label):
		''' sets the string label of
		    the menu mid (by ID within the parent menu tree) '''
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("label", label)

	def setRefId(self, parent, mid, new_id):
		''' sets the id attribute of
		    the menu mid (by ID within the parent menu tree) '''
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("id", new_id)
	
	def setSepLabel(self, menu, num, label=None):
		''' sets the label attribute of a separator
		    pass None to remove label attribute '''
		nodo = self._get_dom_item(menu, num)
		if label is None:
			if nodo.hasAttribute("label"):
				nodo.removeAttribute("label")
		else:
			nodo.setAttribute("label", label)
	
	def setMenuExecute(self, parent, mid, execute):
		''' sets the execute attribute (the attribute NOT the execute tag)
		    of the menu mid (by ID within the parent menu tree) '''
		prnt = self._get_dom_menu(parent)
		if prnt: mnu = self._get_dom_ref(mid, prnt)
		if mnu: mnu.setAttribute("execute", execute)
	
	def getItem(self,menu,num):
		''' Return just an item, given its parent menu and its number '''
		mnu = self._get_dom_menu(menu)
		if not mnu: return
		n = 0
		for i in mnu.childNodes:
			if i.nodeType == 1:
				if n == num:
					if i.nodeName == "menu":
						return self._get_menu_props(i)
					elif i.nodeName == "separator":
						return self._get_sep_props(i)
					elif i.nodeName == "item":
						return self._get_item_props(i) #BUGFIX was missing _
				n += 1
	
	def isMenu(self,menu):
		''' Returns True if it's an existing ID '''
		dom = self._get_dom_menu(menu)
		if dom:
			return True
		else:
			return False
		
	def getMenu(self,menu):
		''' Returns a menu, as a list of dictionaries, not recursively.
		    Each dictionary has the item's properties. '''
		lst = []
		if menu is not None: #BUGFIX was `if menu`
			mnu = self._get_dom_menu(menu)
			if mnu is None:
				mnu = self.dom.documentElement #BUGFIX was `return`
		else:
			mnu = self.dom.documentElement
		for i in mnu.childNodes:
			if i.nodeType == 1:
				if i.nodeName == "menu":
					d = self._get_menu_props(i)
				elif i.nodeName == "separator":
					d = self._get_sep_props(i)
				elif i.nodeName == "item":
					d = self._get_item_props(i)
				d["parent"] = menu		
				lst.append(d)
		return lst

	def getMenuRecursive(self, menuid):
		''' Returns a whole menu, as a list of dictionaries.
		    Each dictionary has the item's properties.
		    Recursively includes lists of dictionaries for the contents of
		    menus, with "." as the key for the contents, because "." can't be
		    an XML tag or attribute and is a symbol for a directory itself. '''
		menu_content = self.menu.getMenu(menuid)
		for it in menu_content:
			if (it["type"] == "menu" and it["action"] != "Pipemenu"
			    and it["action"] != "Link"):
				it["."] = self.getMenuRecursive(it["id"])
		return menu_content

	def replaceId(self, old_id, new_id, parent=None):
		''' replaces all id's in menu matching old_id with new_id
		    parent should be omitted, or it only affects menus under parent '''
		if not parent: parent = self.dom.documentElement
		for item in parent.childNodes:
			if item.nodeName == "menu":
				if item.attributes["id"].nodeValue == old_id:
					item.setAttribute("id", new_id)
				elif item.hasChildNodes():
					self.replaceId(old_id, new_id, item)

