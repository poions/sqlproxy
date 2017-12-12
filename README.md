# sqlproxy
sqlproxy是一款被动式SQL注入扫描器，通过wyproxy代理获取浏览信息---->入库----->出库------>检测------>结果，这样的方式来自动化获取SQL注入
漏洞。                                                                                         
它是基于猪猪侠开发的wyproxy代理脚本下的注入检测工具，通过调用sqlmapapi来进行SQL注入检测。                                           
使用方式：                                                                                           
  一： 下载搭建wyproxy服务，详情参考https://github.com/ring04h/wyproxy                                                                 
  二： 下载搭建sqlmap，使用到的环境是python2.7。         
  三： 下载sqlproxy。                                                                                                   
  四： 设置好sqlproxy数据库连接                                                              
  五： 开启sqlmapapi.py -s                                       
  六： 开启wyproxy  方式：wyproxy.py -p 8888                                                            
                                                                                    
  最后直接运行python sqlproxy.py 
  运行后5秒开始进行对数据库Url的提取检测。
  
                   
                   
  
                                           
  非常感谢延华的大力帮       
  
  
  
                                                          
