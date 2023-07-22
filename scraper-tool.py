#written by 'hafsi youssef' contact: hafsiyoussef07@gmail.com

from microsoft import micro
from amazon import dataweree
from hubspot import hubspot_links_getter
from oracle import datawer
from SAP import spa
from ss import summer
from atlassian import atlassian_scraper,dumperr
import tkinter
from tkinter import * 
f=Tk()
f.title("Scraper Tool")
# f.geometry("205x200") 


path_labels = []
path_entries = [[],[],[],[],[],[],[],[]]
browse_buttons = []
path2_entries=[]
site=['Attlassian','AWS','Hubspot','Microsoft','Oracle','SAP','Smartsheet']


for i in range(7):
    # Create label for filters input field
    path_label = Label(f, text=f"{site[i]} Filters: ",bg="black",fg="white")
    path_label.grid(row=i, column=0, padx=10, pady=5, sticky=W)
    path_labels.append(path_label)

    # Company name
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=1, padx=10, pady=5)
    path_entries[i].append(path_entry)
    path_entry.insert(0, "company_name")

    # location
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=2, padx=10, pady=5)
    path_entry.insert(0, "Location")
    path_entries[i].append(path_entry)

    # country
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=3, padx=10, pady=5)
    path_entry.insert(0, "Country")
    path_entries[i].append(path_entry)

    # specs
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=4, padx=10, pady=5)
    path_entry.insert(0, "specializations")
    path_entries[i].append(path_entry)

    # product
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=5, padx=10, pady=5)
    path_entry.insert(0, "products")
    path_entries[i].append(path_entry)

    # services
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=6, padx=10, pady=5)
    path_entry.insert(0, "services")
    path_entries[i].append(path_entry)

    # Create label for filters input field
    path_label = Label(f, text="Filename :",bg="black",fg="white")
    path_label.grid(row=i, column=8, padx=10, pady=5, sticky=W)
    path_labels.append(path_label)

    # path field
    path_entry =Entry(f.master, width=20)
    path_entry.grid(row=i, column=9, padx=10, pady=5)
    path2_entries.append(path_entry)

    #browser button
    browse_button =Button(f.master, text="Scrape" )
    browse_button.grid(row=i, column=10, padx=10, pady=5)
    browse_buttons.append(browse_button)
for i in range(1,7):
    for j in range(6):
        path_entries[i][j].delete(0,tkinter.END)


browse_buttons[0][COMMAND]=lambda: dumperr(atlassian_scraper(path_entries[0][0].get(),path_entries[0][1].get(),path_entries[0][2].get(),path_entries[0][3].get(),path_entries[0][4].get(),path_entries[0][5].get()),path2_entries[0].get())
browse_buttons[1][COMMAND]=lambda: dumperr(dataweree(path_entries[1][0].get(),path_entries[1][1].get(),path_entries[1][2].get(),path_entries[1][3].get(),path_entries[1][4].get(),path_entries[1][5].get()),path2_entries[1].get())
browse_buttons[2][COMMAND]= lambda:dumperr(hubspot_links_getter(path_entries[2][0].get(),path_entries[2][1].get(),path_entries[2][2].get(),path_entries[2][3].get(),path_entries[2][4].get(),path_entries[2][5].get()),path2_entries[2].get())
browse_buttons[3][COMMAND]= lambda:dumperr(micro(path_entries[3][0].get(),path_entries[3][1].get(),path_entries[3][2].get(),path_entries[3][3].get(),path_entries[3][4].get(),path_entries[3][5].get()),path2_entries[3].get())
browse_buttons[4][COMMAND]= lambda:dumperr(datawer(path_entries[4][0].get(),path_entries[4][1].get(),path_entries[4][2].get(),path_entries[4][3].get(),path_entries[4][4].get(),path_entries[4][5].get()),path2_entries[4].get())
browse_buttons[5][COMMAND]= lambda:dumperr(spa(path_entries[5][0].get(),path_entries[5][1].get(),path_entries[5][2].get(),path_entries[5][3].get(),path_entries[5][4].get(),path_entries[5][5].get()),path2_entries[5].get())
browse_buttons[6][COMMAND]= lambda:dumperr(summer(path_entries[6][0].get(),path_entries[6][1].get(),path_entries[6][2].get(),path_entries[6][3].get(),path_entries[6][4].get(),path_entries[6][5].get()),path2_entries[6].get())


f["bg"]="black"
f.mainloop()