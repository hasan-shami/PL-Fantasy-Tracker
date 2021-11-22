import matplotlib.pyplot as plt
import pandas as pd

master_df = pd.read_excel("FPL_Master.xlsx")

Salahdf=master_df[master_df['Name']=='Salah']
ax1 = plt.gca()
color='green'
ax1.set_ylabel('Cost',color=color)
Salahdf.plot(x='Date',y='Cost',ax=ax1,color=color)

ax2 = ax1.twinx()
color='blue'
ax2.set_ylabel('Form',color=color)
Salahdf.plot(x='Date',y='Form',ax=ax2,color=color)
plt.title('Mohamad Salah: Liverpool, Midfield')

plt.show()