'''
作者: Xioaruan912 xioaruan@gmail.com
最后编辑人员: Xioaruan912 xioaruan@gmail.com
文件作用介绍: 

'''
from  typing  import Any
import httpx
from mcp.server.fastmcp import FastMCP
import shutil
import asyncio 
from loguru import logger
import re
mcp = FastMCP("web_lol")


class ErrorDeal(Exception):
    def __init__(self, mess:str,result:str|None):
        super().__init__(mess)
        self.result = result  
        

async def check_tool(tool :str) -> str:
    tool_dict = ['dirsearch','nmap','afrog']
    if tool not in tool_dict:
        raise ErrorDeal(f"不存在{tool}","tool is not support dirsearch 使用uv pip install --quiet setuptools  安装 nmap 自行安装 afrog 访问 https://github.com/zan8in/afrog 安装")
    # if shutil.which(tool) is None:
    #     logger.info("tool未安装")
    #     raise ErrorDeal(f"{tool}未安装","tool is not install")
    logger.success("tool已经安装")
    return f"{tool} is  available"

@mcp.tool(name="get_tool_list",description="获取可用工具列表")
async def get_tool_list()-> dict:
    """ 获取可使用的 工具列表 
        在开始前需要先调用本工具
    """
    tool_dict = ['dirsearch','nmap','afrog']   
    return tool_dict


async def use_tool(tool:str,url :str) -> str:
    await check_tool(tool=tool)
    if tool == "dirsearch":
        cmd = ['uv','run',tool,"-u",url,"-q"]
        return cmd
    elif tool == "nmap":
        url = re.sub(r's^https?://',"",url,count=1)
        cmd = [tool,url]  
        return cmd
    elif tool == "afrog":
        cmd = ["./tool/"+tool,'-t',url,' -silent']  
        return cmd


@mcp.tool(name="information_search",description="对web进行基本信息扫描")
async def information_search(tool:str,url:str) -> str:
    """ 对传入url 使用 进行扫描 返回扫描结果,并且等待直到结果返回
    args:
        tool:需要使用的工具包含： dirsearch,nmap 
        url: 需要扫描的url 可以是 单个ip
    """
    logger.info("开始检查tool")
    cmd = await use_tool(tool=tool,url=url)
    logger.info("开始执行tool")
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout= asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE  
    )
    out,err = await proc.communicate()
    if proc.returncode == 0:
       return  out.decode().strip()
    else:
        raise ErrorDeal("错误"," error run out ")
    
    
    
if __name__ == "__main__":
    mcp.run(transport="stdio")