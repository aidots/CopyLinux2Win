This software enables the copying of files or internet image links from the host Ubuntu machine, allowing for direct pasting and sending within WeChat on the virtual machine Win10. Software environment: Host machine Ubuntu 20.04.6 LTS, VirtualBox 6.1.38_Ubuntu r153438, with Windows 10 installed.\
\
First, share the Linux folder with the Windows virtual machine and find the mapping relationship. For example, in my case, /media/aigc/Linux/xxx/xxx corresponds to the Win address Z:/xxx/xxx. Then, modify the information like /media/aigc/Linux/ in main.py to match your own setup.\
\
To set up startup on boot:\
Create a shortcut for auto.bat and copy it to the C:\Users\<Your Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup folder.\
\
\
本软件实现从宿主机Ubuntu里复制文件或互联网图片链接，虚拟机Win10里能直接粘贴到微信里发送。软件环境：宿主机Ubuntu20.04.6LTS，虚拟机Virtual Box 6.1.38_Ubuntu r153438，安装的Windows 10。\

首先把linux的文件夹共享给Windows虚拟机，找到映射关系，比如我这里的 /media/aigc/Linux/xxx/xxx 对应Win的地址为 Z:/xxx/xxx，
然后修改main.py里面的/media/aigc/Linux/等信息为你自己的。\
\
设置开机启动：\
将auto.bat新建快捷方式，复制到C:\Users\<Your Username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup文件夹下即可。
