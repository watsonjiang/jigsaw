#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
import gtk
import random

class ImageHandler:
   n_w = 4
   n_h = 4
   def __init__(self, file_, w, h):
      self.pixbuf = gtk.gdk.pixbuf_new_from_file(file_)
      self.pixbuf = self.pixbuf.scale_simple(w, h, gtk.gdk.INTERP_BILINEAR) 
      self.pixbuf1 = gtk.gdk.Pixbuf(self.pixbuf.get_colorspace(),
                                    self.pixbuf.get_has_alpha(),
                                    self.pixbuf.get_bits_per_sample(),
                                    w, h)
      self.w = w
      self.h = h
      self.matrix = [i for i in xrange(0, self.n_w * self.n_h)]
      

   def shuffle(self):
      random.shuffle(self.matrix) 

   def swap(self, idx1, idx2):
      self.matrix[idx1], self.matrix[idx2] = \
                                 self.matrix[idx2], self.matrix[idx1]

   def is_reordered(self):
      for i in xrange(0, self.n_w * self.n_h):
         if i != self.matrix[i]:
            return False
      return True

   def get_i_w(self):
      return self.w / self.n_w

   def get_i_h(self):
      return self.h / self.n_h

   def get_img(self):
      i_w = self.w / self.n_w
      i_h = self.h / self.n_h
      for i in xrange(0, self.n_w * self.n_h):
         k = self.matrix[i]
         kx = (k % self.n_h) * i_w
         ky = (k / self.n_h) * i_h
         mx = (i % self.n_h) * i_w
         my = (i / self.n_h) * i_h
         self.pixbuf.copy_area(kx, ky, i_w, i_h, self.pixbuf1, mx, my)

      return self.pixbuf1 
       

class MainFrame:
   def delete_event(self, widget, event, data=None):
      # If you return FALSE in the "delete_event" signal handler,
      # GTK will emit the "destroy" signal. Returning TRUE means
      # you don't want the window to be destroyed.
      # This is useful for popping up 'are you sure you want to quit?'
      # type dialogs.
      print "delete event occurred"

      # Change FALSE to TRUE and the main window will not be destroyed
      # with a "delete_event".
      return False

   def destroy(self, widget, data=None):
      print "destroy signal occurred"
      gtk.main_quit()

   def on_click(self, widget, event):
      i_x = int(event.x) / self.ih.get_i_w()
      i_y = int(event.y) / self.ih.get_i_h()
      if self.selected == None:
         self.selected = (i_x, i_y) 
         gc = widget.style.white_gc
         x = i_x * self.ih.get_i_w()
         y = i_y * self.ih.get_i_h()
         self.pixmap.draw_rectangle(gc, False, x, y, self.ih.get_i_w(), self.ih.get_i_h())
      else:
         idx1 = i_x + i_y * self.ih.n_h
         idx2 = self.selected[0] + self.selected[1] * self.ih.n_h
         self.ih.swap(idx1, idx2)
         gc = widget.style.white_gc
         self.pixmap.draw_pixbuf(gc, self.ih.get_img(), 0, 0, 0, 0)
         self.selected = None
      
      widget.queue_draw_area(0, 0, 600, 600) 
      if self.ih.is_reordered():
         self.on_success(widget)


   def on_success(self, widget):
      dlg = gtk.MessageDialog(type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
      dlg.set_markup("success!")
      dlg.run()
      dlg.destroy() 
      self.load_image()
      gc = widget.style.white_gc
      self.pixmap.draw_pixbuf(gc, self.ih.get_img(), 0, 0, 0, 0)
      widget.queue_draw_area(0, 0, 600, 600) 


   def on_draw(self, widget, event):
      gc = widget.style.white_gc
      x, y, w, h = event.area
      widget.window.draw_drawable(gc, self.pixmap, x, y, x, y, w, h)

   def load_image(self):
      #files = ['car.jpg', 'truck.png']
      files = ['car.jpg']
      f = random.choice(files)
      self.ih = ImageHandler(f, 600,600)
      self.ih.shuffle()

   def __init__(self):
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.add_events(gtk.gdk.BUTTON_PRESS_MASK)
      self.window.connect('delete_event', self.delete_event)
      self.window.connect('destroy', self.destroy)
      self.window.connect('button-press-event', self.on_click) 
      self.window.set_resizable(False)
      self.darea = gtk.DrawingArea()
      self.darea.set_size_request(600, 600)
      self.darea.connect('expose-event', self.on_draw) 
      self.window.add(self.darea)
      self.window.show_all()
      self.load_image()
      self.pixmap = gtk.gdk.Pixmap(self.window.window, 600, 600)
      gc = self.window.style.white_gc
      self.pixmap.draw_pixbuf(gc, self.ih.get_img(), 0, 0, 0, 0)
      self.selected = None 


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
   main_frm = MainFrame()
   gtk.main()
