import json
import shlex
import subprocess
import sys

from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List

router = APIRouter()


@router.post("/extract_from_url")
def extract_from_url(urls: List[str], max_next_pages: int = 0) -> List[Dict[str, Any]]:
    """Extract content from a list of urls. 

    Args:   
        urls (List[str]): single url or list of urls to be searched   
        max_next_pages (int): number of next pages to be searched (default: 0 = disable navigation to next pages)  

    Returns:   
        (List[Dict[str, Any]]): a list of dict objects scraped from the url(s)   

    """
    # Validate urls input
    if len(urls) == 0:
        raise HTTPException(status_code=400, detail="URL cannot be empty")

    # launch spider by command line
    cmd: str = f"{sys.executable} -m scrapy_project.web_extraction.spiders.generic_spider --urls_to_query \"{list(urls)}\" --max_next_pages \"{max_next_pages}\""
    cmd = shlex.split(cmd)
    output = subprocess.check_output(cmd, timeout=5 * 60)

    # return the results
    all_contents = [json.loads(el) for el in output.decode("utf-8").split("\n") if len(el) > 0]
    
    return all_contents


@router.post("/extract_from_trustpilot_url")
def extract_from_trustpilot_url(suffix: str, language: str = "all", max_next_pages: int = 0) -> List[Dict[str, Any]]:
    """
    Extract content from the trustpilot url (https://www.trustpilot.com/review)

    Args:   
        suffix (str): the suffix of the url (https://www.trustpilot.com/review/<suffix>)   
        language (str): the language to be searched (default: all)   
        max_next_pages (int): the maximum number of next pages to be searched (default: 0 = no next pages)    

    Returns:   
        (List[Dict[str, Any]]): a list of dict objects scraped from the url(s)

    """
    # Validate suffix input
    if len(suffix) == 0:
        raise HTTPException(status_code=400, detail="Suffix cannot be empty")

    # launch spider by command line
    cmd: str = f"{sys.executable} -m scrapy_project.web_extraction.spiders.trustpilot_spider --suffix \"{suffix}\" --language \"{language}\" --max_next_pages \"{max_next_pages}\""
    cmd = shlex.split(cmd)
    output = subprocess.check_output(cmd,timeout=5 * 60)

    # return the results
    all_contents = [json.loads(el) for el in output.decode("utf-8").split("\n") if len(el) > 0]

    return all_contents
