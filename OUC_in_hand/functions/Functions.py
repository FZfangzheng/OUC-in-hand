#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import execjs
import re
from bs4 import BeautifulSoup
import base64
import hashlib
# import matplotlib.pyplot as plt
# from Thread import *
from functions import Thread

class Function:
    def __init__(self, numberid, url, sessionid, deskey, nowtime):
        self.__numberid = numberid
        self.__nowUrl = url
        self.__sessionid = sessionid
        self.__deskey = deskey
        self.__nowtime = nowtime
        self.__xn = '2018'
        self.__xq = '0'

    @property
    def nowtime(self):
        return self.__nowtime

    @nowtime.setter
    def nowtime(self, time):
        self.__nowtime = time

    @property
    def deskey(self):
        return self.__deskey

    @nowtime.setter
    def deskey(self, desky):
        self.__deskey = desky

    @property
    def nowUrl(self):
        return self.__nowUrl

    @nowUrl.setter
    def nowUrl(self, url):
        self.__nowUrl = url

    @property
    def xn(self):
        return self.__xn

    @xn.setter
    def xn(self, xn):
        self.__xn = xn

    @property
    def xq(self):
        return self.__xq

    @xq.setter
    def xq(self, xq):
        self.__xq = xq

    def changTime(self):
        timeId = input("输入你要选择的时间序号：\n1.2018秋季学期\n2.2018夏季学期\n3.2018春季学期\n"
              "4.2017秋季学期\n5.2017夏季学期\n6.2017春季学期\n"
              "7.2016秋季学期\n")
        if timeId == "1":
            self.xn = "2018"
            self.xq = "1"
        if timeId == "2":
            self.xn = "2018"
            self.xq = "0"
        if timeId == "3":
            self.xn = "2017"
            self.xq = "2"
        if timeId == "4":
            self.xn = "2017"
            self.xq = "1"
        if timeId == "5":
            self.xn = "2017"
            self.xq = "0"
        if timeId == "6":
            self.xn = "2016"
            self.xq = "2"
        if timeId == "7":
            self.xn = "2016"
            self.xq = "1"

    # 查询成绩
    def InquiryGrades(self, xn, xq, xh, xnxq):
        # xn = '2016'  # 学期
        #         # xn1 = '2018'  # 现在年份
        #         # xq = '2'
        #         # ysyx = 'yscj'  # 原始成绩，yxjc是有效成绩
        #         # sjxz = 'sjxz1'  # 入学以来，sjxz3是学期
        #         # userCode = self.__numberid
        try:
            s = requests.Session()
            cookies = {'JSESSIONID': self.__sessionid}
            header = {
                'Host': self.__nowUrl,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://' + self.__nowUrl + '/cas/login.action',
                'Connection': 'keep-alive'
            }
            SetKingoEncyptContent = s.get('http://' + self.__nowUrl + '/custom/js/SetKingoEncypt.jsp', headers=header,
                                          cookies=cookies, timeout=300)
            SetKingoEncyptContent.raise_for_status()
            content = SetKingoEncyptContent.text
            _deskey = content.split("\n", 4)[2].split("'", 3)[1]
            _nowtime = content.split("\n", 4)[3].split("'", 3)[1]
            self.__deskey = _deskey
            self.__nowtime = _nowtime
        except:
            print("Error happened in getDeskeyAndNowtime()")
        if xn == "0000":
            params = "xn=2017&xn1=2018&xq=2&ysyx=yscj&sjxz=sjxz1&userCode="+xh+"&ysyxS=on&sjxzS=on"
        else:
            params = "xn="+xn+"&xn1=2018&xq="+xq+"&ysyx=yscj&sjxz=sjxz3&userCode="+xh+"&xnxq="+xnxq+"&ysyxS=on&sjxzS=on"
        # 加密参数
        hl = hashlib.md5()
        hl.update(params.encode(encoding='utf-8'))
        enparams = str(hl.hexdigest())
        hl = hashlib.md5()
        # hl.update("2018-07-16 10:43:34".encode(encoding='utf-8'))
        hl.update(self.__nowtime.encode(encoding='utf-8'))
        entime = str(hl.hexdigest())
        hl = hashlib.md5()
        hl.update((enparams+entime).encode(encoding='utf-8'))
        token = str(hl.hexdigest())
        # token从str转到byte
        functionStrEnc = """function strEnc(data,firstKey,secondKey,thirdKey){

 var leng = data.length;
 var encData = "";
 var firstKeyBt,secondKeyBt,thirdKeyBt,firstLength,secondLength,thirdLength;
 if(firstKey != null && firstKey != ""){    
   firstKeyBt = getKeyBytes(firstKey);
   firstLength = firstKeyBt.length;
 }
 if(secondKey != null && secondKey != ""){
   secondKeyBt = getKeyBytes(secondKey);
   secondLength = secondKeyBt.length;
 }
 if(thirdKey != null && thirdKey != ""){
   thirdKeyBt = getKeyBytes(thirdKey);
   thirdLength = thirdKeyBt.length;
 }  
 
 if(leng > 0){
   if(leng < 4){
     var bt = strToBt(data);      
     var encByte ;
     if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){
       var tempBt;
       var x,y,z;
       tempBt = bt;        
       for(x = 0;x < firstLength ;x ++){
         tempBt = enc(tempBt,firstKeyBt[x]);
       }
       for(y = 0;y < secondLength ;y ++){
         tempBt = enc(tempBt,secondKeyBt[y]);
       }
       for(z = 0;z < thirdLength ;z ++){
         tempBt = enc(tempBt,thirdKeyBt[z]);
       }        
       encByte = tempBt;        
     }else{
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){
         var tempBt;
         var x,y;
         tempBt = bt;
         for(x = 0;x < firstLength ;x ++){
           tempBt = enc(tempBt,firstKeyBt[x]);
         }
         for(y = 0;y < secondLength ;y ++){
           tempBt = enc(tempBt,secondKeyBt[y]);
         }
         encByte = tempBt;
       }else{
         if(firstKey != null && firstKey !=""){            
           var tempBt;
           var x = 0;
           tempBt = bt;            
           for(x = 0;x < firstLength ;x ++){
             tempBt = enc(tempBt,firstKeyBt[x]);
           }
           encByte = tempBt;
         }
       }        
     }
     encData = bt64ToHex(encByte);
   }else{
     var iterator = parseInt(leng/4);
     var remainder = leng%4;
     var i=0;      
     for(i = 0;i < iterator;i++){
       var tempData = data.substring(i*4+0,i*4+4);
       var tempByte = strToBt(tempData);
       var encByte ;
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){
         var tempBt;
         var x,y,z;
         tempBt = tempByte;
         for(x = 0;x < firstLength ;x ++){
           tempBt = enc(tempBt,firstKeyBt[x]);
         }
         for(y = 0;y < secondLength ;y ++){
           tempBt = enc(tempBt,secondKeyBt[y]);
         }
         for(z = 0;z < thirdLength ;z ++){
           tempBt = enc(tempBt,thirdKeyBt[z]);
         }
         encByte = tempBt;
       }else{
         if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){
           var tempBt;
           var x,y;
           tempBt = tempByte;
           for(x = 0;x < firstLength ;x ++){
             tempBt = enc(tempBt,firstKeyBt[x]);
           }
           for(y = 0;y < secondLength ;y ++){
             tempBt = enc(tempBt,secondKeyBt[y]);
           }
           encByte = tempBt;
         }else{
           if(firstKey != null && firstKey !=""){                      
             var tempBt;
             var x;
             tempBt = tempByte;
             for(x = 0;x < firstLength ;x ++){                
               tempBt = enc(tempBt,firstKeyBt[x]);
             }
             encByte = tempBt;              
           }
         }
       }
       encData += bt64ToHex(encByte);
     }      
     if(remainder > 0){
       var remainderData = data.substring(iterator*4+0,leng);
       var tempByte = strToBt(remainderData);
       var encByte ;
       if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){
         var tempBt;
         var x,y,z;
         tempBt = tempByte;
         for(x = 0;x < firstLength ;x ++){
           tempBt = enc(tempBt,firstKeyBt[x]);
         }
         for(y = 0;y < secondLength ;y ++){
           tempBt = enc(tempBt,secondKeyBt[y]);
         }
         for(z = 0;z < thirdLength ;z ++){
           tempBt = enc(tempBt,thirdKeyBt[z]);
         }
         encByte = tempBt;
       }else{
         if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){
           var tempBt;
           var x,y;
           tempBt = tempByte;
           for(x = 0;x < firstLength ;x ++){
             tempBt = enc(tempBt,firstKeyBt[x]);
           }
           for(y = 0;y < secondLength ;y ++){
             tempBt = enc(tempBt,secondKeyBt[y]);
           }
           encByte = tempBt;
         }else{
           if(firstKey != null && firstKey !=""){            
             var tempBt;
             var x;
             tempBt = tempByte;
             for(x = 0;x < firstLength ;x ++){
               tempBt = enc(tempBt,firstKeyBt[x]);
             }
             encByte = tempBt;
           }
         }
       }
       encData += bt64ToHex(encByte);
     }                
   }
 }
 return encData;
}

/*
* DES解密
* decrypt the encrypted string to the original string 
* return  the original string  
*/
function strDec(data,firstKey,secondKey,thirdKey){
 var leng = data.length;
 var decStr = "";
 var firstKeyBt,secondKeyBt,thirdKeyBt,firstLength,secondLength,thirdLength;
 if(firstKey != null && firstKey != ""){    
   firstKeyBt = getKeyBytes(firstKey);
   firstLength = firstKeyBt.length;
 }
 if(secondKey != null && secondKey != ""){
   secondKeyBt = getKeyBytes(secondKey);
   secondLength = secondKeyBt.length;
 }
 if(thirdKey != null && thirdKey != ""){
   thirdKeyBt = getKeyBytes(thirdKey);
   thirdLength = thirdKeyBt.length;
 }
 
 var iterator = parseInt(leng/16);
 var i=0;  
 for(i = 0;i < iterator;i++){
   var tempData = data.substring(i*16+0,i*16+16);    
   var strByte = hexToBt64(tempData);    
   var intByte = new Array(64);
   var j = 0;
   for(j = 0;j < 64; j++){
     intByte[j] = parseInt(strByte.substring(j,j+1));
   }    
   var decByte;
   if(firstKey != null && firstKey !="" && secondKey != null && secondKey != "" && thirdKey != null && thirdKey != ""){
     var tempBt;
     var x,y,z;
     tempBt = intByte;
     for(x = thirdLength - 1;x >= 0;x --){
       tempBt = dec(tempBt,thirdKeyBt[x]);
     }
     for(y = secondLength - 1;y >= 0;y --){
       tempBt = dec(tempBt,secondKeyBt[y]);
     }
     for(z = firstLength - 1;z >= 0 ;z --){
       tempBt = dec(tempBt,firstKeyBt[z]);
     }
     decByte = tempBt;
   }else{
     if(firstKey != null && firstKey !="" && secondKey != null && secondKey != ""){
       var tempBt;
       var x,y,z;
       tempBt = intByte;
       for(x = secondLength - 1;x >= 0 ;x --){
         tempBt = dec(tempBt,secondKeyBt[x]);
       }
       for(y = firstLength - 1;y >= 0 ;y --){
         tempBt = dec(tempBt,firstKeyBt[y]);
       }
       decByte = tempBt;
     }else{
       if(firstKey != null && firstKey !=""){
         var tempBt;
         var x,y,z;
         tempBt = intByte;
         for(x = firstLength - 1;x >= 0 ;x --){
           tempBt = dec(tempBt,firstKeyBt[x]);
         }
         decByte = tempBt;
       }
     }
   }
   decStr += byteToString(decByte);
 }      
 return decStr;
}
/*
* chang the string into the bit array
* 
* return bit array(it's length % 64 = 0)
*/
function getKeyBytes(key){
 var keyBytes = new Array();
 var leng = key.length;
 var iterator = parseInt(leng/4);
 var remainder = leng%4;
 var i = 0;
 for(i = 0;i < iterator; i ++){
   keyBytes[i] = strToBt(key.substring(i*4+0,i*4+4));
 }
 if(remainder > 0){
   keyBytes[i] = strToBt(key.substring(i*4+0,leng));
 }    
 return keyBytes;
}

/*
* chang the string(it's length <= 4) into the bit array
* 
* return bit array(it's length = 64)
*/
function strToBt(str){  
 var leng = str.length;
 var bt = new Array(64);
 if(leng < 4){
   var i=0,j=0,p=0,q=0;
   for(i = 0;i<leng;i++){
     var k = str.charCodeAt(i);
     for(j=0;j<16;j++){      
       var pow=1,m=0;
       for(m=15;m>j;m--){
         pow *= 2;
       }        
       bt[16*i+j]=parseInt(k/pow)%2;
     }
   }
   for(p = leng;p<4;p++){
     var k = 0;
     for(q=0;q<16;q++){      
       var pow=1,m=0;
       for(m=15;m>q;m--){
         pow *= 2;
       }        
       bt[16*p+q]=parseInt(k/pow)%2;
     }
   }  
 }else{
   for(i = 0;i<4;i++){
     var k = str.charCodeAt(i);
     for(j=0;j<16;j++){      
       var pow=1;
       for(m=15;m>j;m--){
         pow *= 2;
       }        
       bt[16*i+j]=parseInt(k/pow)%2;
     }
   }  
 }
 return bt;
}

/*
* chang the bit(it's length = 4) into the hex
* 
* return hex
*/
function bt4ToHex(binary) {
 var hex;
 switch (binary) {
   case "0000" : hex = "0"; break;
   case "0001" : hex = "1"; break;
   case "0010" : hex = "2"; break;
   case "0011" : hex = "3"; break;
   case "0100" : hex = "4"; break;
   case "0101" : hex = "5"; break;
   case "0110" : hex = "6"; break;
   case "0111" : hex = "7"; break;
   case "1000" : hex = "8"; break;
   case "1001" : hex = "9"; break;
   case "1010" : hex = "A"; break;
   case "1011" : hex = "B"; break;
   case "1100" : hex = "C"; break;
   case "1101" : hex = "D"; break;
   case "1110" : hex = "E"; break;
   case "1111" : hex = "F"; break;
 }
 return hex;
}

/*
* chang the hex into the bit(it's length = 4)
* 
* return the bit(it's length = 4)
*/
function hexToBt4(hex) {
 var binary;
 switch (hex) {
   case "0" : binary = "0000"; break;
   case "1" : binary = "0001"; break;
   case "2" : binary = "0010"; break;
   case "3" : binary = "0011"; break;
   case "4" : binary = "0100"; break;
   case "5" : binary = "0101"; break;
   case "6" : binary = "0110"; break;
   case "7" : binary = "0111"; break;
   case "8" : binary = "1000"; break;
   case "9" : binary = "1001"; break;
   case "A" : binary = "1010"; break;
   case "B" : binary = "1011"; break;
   case "C" : binary = "1100"; break;
   case "D" : binary = "1101"; break;
   case "E" : binary = "1110"; break;
   case "F" : binary = "1111"; break;
 }
 return binary;
}

/*
* chang the bit(it's length = 64) into the string
* 
* return string
*/
function byteToString(byteData){
 var str="";
 for(i = 0;i<4;i++){
   var count=0;
   for(j=0;j<16;j++){        
     var pow=1;
     for(m=15;m>j;m--){
       pow*=2;
     }              
     count+=byteData[16*i+j]*pow;
   }        
   if(count != 0){
     str+=String.fromCharCode(count);
   }
 }
 return str;
}

function bt64ToHex(byteData){
 var hex = "";
 for(i = 0;i<16;i++){
   var bt = "";
   for(j=0;j<4;j++){    
     bt += byteData[i*4+j];
   }    
   hex+=bt4ToHex(bt);
 }
 return hex;
}

function hexToBt64(hex){
 var binary = "";
 for(i = 0;i<16;i++){
   binary+=hexToBt4(hex.substring(i,i+1));
 }
 return binary;
}

/*
* the 64 bit des core arithmetic
*/

function enc(dataByte,keyByte){  
 var keys = generateKeys(keyByte);    
 var ipByte   = initPermute(dataByte);  
 var ipLeft   = new Array(32);
 var ipRight  = new Array(32);
 var tempLeft = new Array(32);
 var i = 0,j = 0,k = 0,m = 0, n = 0;
 for(k = 0;k < 32;k ++){
   ipLeft[k] = ipByte[k];
   ipRight[k] = ipByte[32+k];
 }    
 for(i = 0;i < 16;i ++){
   for(j = 0;j < 32;j ++){
     tempLeft[j] = ipLeft[j];
     ipLeft[j] = ipRight[j];      
   }  
   var key = new Array(48);
   for(m = 0;m < 48;m ++){
     key[m] = keys[i][m];
   }
   var  tempRight = xor(pPermute(sBoxPermute(xor(expandPermute(ipRight),key))), tempLeft);      
   for(n = 0;n < 32;n ++){
     ipRight[n] = tempRight[n];
   }  
   
 }  
 
 
 var finalData =new Array(64);
 for(i = 0;i < 32;i ++){
   finalData[i] = ipRight[i];
   finalData[32+i] = ipLeft[i];
 }
 return finallyPermute(finalData);  
}

function dec(dataByte,keyByte){  
 var keys = generateKeys(keyByte);    
 var ipByte   = initPermute(dataByte);  
 var ipLeft   = new Array(32);
 var ipRight  = new Array(32);
 var tempLeft = new Array(32);
 var i = 0,j = 0,k = 0,m = 0, n = 0;
 for(k = 0;k < 32;k ++){
   ipLeft[k] = ipByte[k];
   ipRight[k] = ipByte[32+k];
 }  
 for(i = 15;i >= 0;i --){
   for(j = 0;j < 32;j ++){
     tempLeft[j] = ipLeft[j];
     ipLeft[j] = ipRight[j];      
   }  
   var key = new Array(48);
   for(m = 0;m < 48;m ++){
     key[m] = keys[i][m];
   }
   
   var  tempRight = xor(pPermute(sBoxPermute(xor(expandPermute(ipRight),key))), tempLeft);      
   for(n = 0;n < 32;n ++){
     ipRight[n] = tempRight[n];
   }  
 }  
 
 
 var finalData =new Array(64);
 for(i = 0;i < 32;i ++){
   finalData[i] = ipRight[i];
   finalData[32+i] = ipLeft[i];
 }
 return finallyPermute(finalData);  
}

function initPermute(originalData){
 var ipByte = new Array(64);
 for (i = 0, m = 1, n = 0; i < 4; i++, m += 2, n += 2) {
   for (j = 7, k = 0; j >= 0; j--, k++) {
     ipByte[i * 8 + k] = originalData[j * 8 + m];
     ipByte[i * 8 + k + 32] = originalData[j * 8 + n];
   }
 }    
 return ipByte;
}

function expandPermute(rightData){  
 var epByte = new Array(48);
 for (i = 0; i < 8; i++) {
   if (i == 0) {
     epByte[i * 6 + 0] = rightData[31];
   } else {
     epByte[i * 6 + 0] = rightData[i * 4 - 1];
   }
   epByte[i * 6 + 1] = rightData[i * 4 + 0];
   epByte[i * 6 + 2] = rightData[i * 4 + 1];
   epByte[i * 6 + 3] = rightData[i * 4 + 2];
   epByte[i * 6 + 4] = rightData[i * 4 + 3];
   if (i == 7) {
     epByte[i * 6 + 5] = rightData[0];
   } else {
     epByte[i * 6 + 5] = rightData[i * 4 + 4];
   }
 }      
 return epByte;
}

function xor(byteOne,byteTwo){  
 var xorByte = new Array(byteOne.length);
 for(i = 0;i < byteOne.length; i ++){      
   xorByte[i] = byteOne[i] ^ byteTwo[i];
 }  
 return xorByte;
}

function sBoxPermute(expandByte){
 
   var sBoxByte = new Array(32);
   var binary = "";
   var s1 = [
       [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
       [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
       [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
       [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]];

       /* Table - s2 */
   var s2 = [
       [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
       [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
       [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
       [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]];

       /* Table - s3 */
   var s3= [
       [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
       [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
       [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
       [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]];
       /* Table - s4 */
   var s4 = [
       [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
       [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
       [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
       [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14 ]];

       /* Table - s5 */
   var s5 = [
       [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
       [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
       [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
       [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]];

       /* Table - s6 */
   var s6 = [
       [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
       [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
       [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
       [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13 ]];

       /* Table - s7 */
   var s7 = [
       [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
       [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
       [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
       [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]];

       /* Table - s8 */
   var s8 = [
       [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
       [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
       [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
       [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]];
   
   for(m=0;m<8;m++){
   var i=0,j=0;
   i = expandByte[m*6+0]*2+expandByte[m*6+5];
   j = expandByte[m * 6 + 1] * 2 * 2 * 2 
     + expandByte[m * 6 + 2] * 2* 2 
     + expandByte[m * 6 + 3] * 2 
     + expandByte[m * 6 + 4];
   switch (m) {
     case 0 :
       binary = getBoxBinary(s1[i][j]);
       break;
     case 1 :
       binary = getBoxBinary(s2[i][j]);
       break;
     case 2 :
       binary = getBoxBinary(s3[i][j]);
       break;
     case 3 :
       binary = getBoxBinary(s4[i][j]);
       break;
     case 4 :
       binary = getBoxBinary(s5[i][j]);
       break;
     case 5 :
       binary = getBoxBinary(s6[i][j]);
       break;
     case 6 :
       binary = getBoxBinary(s7[i][j]);
       break;
     case 7 :
       binary = getBoxBinary(s8[i][j]);
       break;
   }      
   sBoxByte[m*4+0] = parseInt(binary.substring(0,1));
   sBoxByte[m*4+1] = parseInt(binary.substring(1,2));
   sBoxByte[m*4+2] = parseInt(binary.substring(2,3));
   sBoxByte[m*4+3] = parseInt(binary.substring(3,4));
 }
 return sBoxByte;
}

function pPermute(sBoxByte){
 var pBoxPermute = new Array(32);
 pBoxPermute[ 0] = sBoxByte[15]; 
 pBoxPermute[ 1] = sBoxByte[ 6]; 
 pBoxPermute[ 2] = sBoxByte[19]; 
 pBoxPermute[ 3] = sBoxByte[20]; 
 pBoxPermute[ 4] = sBoxByte[28]; 
 pBoxPermute[ 5] = sBoxByte[11]; 
 pBoxPermute[ 6] = sBoxByte[27]; 
 pBoxPermute[ 7] = sBoxByte[16]; 
 pBoxPermute[ 8] = sBoxByte[ 0]; 
 pBoxPermute[ 9] = sBoxByte[14]; 
 pBoxPermute[10] = sBoxByte[22]; 
 pBoxPermute[11] = sBoxByte[25]; 
 pBoxPermute[12] = sBoxByte[ 4]; 
 pBoxPermute[13] = sBoxByte[17]; 
 pBoxPermute[14] = sBoxByte[30]; 
 pBoxPermute[15] = sBoxByte[ 9]; 
 pBoxPermute[16] = sBoxByte[ 1]; 
 pBoxPermute[17] = sBoxByte[ 7]; 
 pBoxPermute[18] = sBoxByte[23]; 
 pBoxPermute[19] = sBoxByte[13]; 
 pBoxPermute[20] = sBoxByte[31]; 
 pBoxPermute[21] = sBoxByte[26]; 
 pBoxPermute[22] = sBoxByte[ 2]; 
 pBoxPermute[23] = sBoxByte[ 8]; 
 pBoxPermute[24] = sBoxByte[18]; 
 pBoxPermute[25] = sBoxByte[12]; 
 pBoxPermute[26] = sBoxByte[29]; 
 pBoxPermute[27] = sBoxByte[ 5]; 
 pBoxPermute[28] = sBoxByte[21]; 
 pBoxPermute[29] = sBoxByte[10]; 
 pBoxPermute[30] = sBoxByte[ 3]; 
 pBoxPermute[31] = sBoxByte[24];    
 return pBoxPermute;
}

function finallyPermute(endByte){    
 var fpByte = new Array(64);  
 fpByte[ 0] = endByte[39]; 
 fpByte[ 1] = endByte[ 7]; 
 fpByte[ 2] = endByte[47]; 
 fpByte[ 3] = endByte[15]; 
 fpByte[ 4] = endByte[55]; 
 fpByte[ 5] = endByte[23]; 
 fpByte[ 6] = endByte[63]; 
 fpByte[ 7] = endByte[31]; 
 fpByte[ 8] = endByte[38]; 
 fpByte[ 9] = endByte[ 6]; 
 fpByte[10] = endByte[46]; 
 fpByte[11] = endByte[14]; 
 fpByte[12] = endByte[54]; 
 fpByte[13] = endByte[22]; 
 fpByte[14] = endByte[62]; 
 fpByte[15] = endByte[30]; 
 fpByte[16] = endByte[37]; 
 fpByte[17] = endByte[ 5]; 
 fpByte[18] = endByte[45]; 
 fpByte[19] = endByte[13]; 
 fpByte[20] = endByte[53]; 
 fpByte[21] = endByte[21]; 
 fpByte[22] = endByte[61]; 
 fpByte[23] = endByte[29]; 
 fpByte[24] = endByte[36]; 
 fpByte[25] = endByte[ 4]; 
 fpByte[26] = endByte[44]; 
 fpByte[27] = endByte[12]; 
 fpByte[28] = endByte[52]; 
 fpByte[29] = endByte[20]; 
 fpByte[30] = endByte[60]; 
 fpByte[31] = endByte[28]; 
 fpByte[32] = endByte[35]; 
 fpByte[33] = endByte[ 3]; 
 fpByte[34] = endByte[43]; 
 fpByte[35] = endByte[11]; 
 fpByte[36] = endByte[51]; 
 fpByte[37] = endByte[19]; 
 fpByte[38] = endByte[59]; 
 fpByte[39] = endByte[27]; 
 fpByte[40] = endByte[34]; 
 fpByte[41] = endByte[ 2]; 
 fpByte[42] = endByte[42]; 
 fpByte[43] = endByte[10]; 
 fpByte[44] = endByte[50]; 
 fpByte[45] = endByte[18]; 
 fpByte[46] = endByte[58]; 
 fpByte[47] = endByte[26]; 
 fpByte[48] = endByte[33]; 
 fpByte[49] = endByte[ 1]; 
 fpByte[50] = endByte[41]; 
 fpByte[51] = endByte[ 9]; 
 fpByte[52] = endByte[49]; 
 fpByte[53] = endByte[17]; 
 fpByte[54] = endByte[57]; 
 fpByte[55] = endByte[25]; 
 fpByte[56] = endByte[32]; 
 fpByte[57] = endByte[ 0]; 
 fpByte[58] = endByte[40]; 
 fpByte[59] = endByte[ 8]; 
 fpByte[60] = endByte[48]; 
 fpByte[61] = endByte[16]; 
 fpByte[62] = endByte[56]; 
 fpByte[63] = endByte[24];
 return fpByte;
}

function getBoxBinary(i) {
 var binary = "";
 switch (i) {
   case 0 :binary = "0000";break;
   case 1 :binary = "0001";break;
   case 2 :binary = "0010";break;
   case 3 :binary = "0011";break;
   case 4 :binary = "0100";break;
   case 5 :binary = "0101";break;
   case 6 :binary = "0110";break;
   case 7 :binary = "0111";break;
   case 8 :binary = "1000";break;
   case 9 :binary = "1001";break;
   case 10 :binary = "1010";break;
   case 11 :binary = "1011";break;
   case 12 :binary = "1100";break;
   case 13 :binary = "1101";break;
   case 14 :binary = "1110";break;
   case 15 :binary = "1111";break;
 }
 return binary;
}
/*
* generate 16 keys for xor
*
*/
function generateKeys(keyByte){    
 var key   = new Array(56);
 var keys = new Array();  
 
 keys[ 0] = new Array();
 keys[ 1] = new Array();
 keys[ 2] = new Array();
 keys[ 3] = new Array();
 keys[ 4] = new Array();
 keys[ 5] = new Array();
 keys[ 6] = new Array();
 keys[ 7] = new Array();
 keys[ 8] = new Array();
 keys[ 9] = new Array();
 keys[10] = new Array();
 keys[11] = new Array();
 keys[12] = new Array();
 keys[13] = new Array();
 keys[14] = new Array();
 keys[15] = new Array();  
 var loop = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1];

 for(i=0;i<7;i++){
   for(j=0,k=7;j<8;j++,k--){
     key[i*8+j]=keyByte[8*k+i];
   }
 }    
 
 var i = 0;
 for(i = 0;i < 16;i ++){
   var tempLeft=0;
   var tempRight=0;
   for(j = 0; j < loop[i];j ++){          
     tempLeft = key[0];
     tempRight = key[28];
     for(k = 0;k < 27 ;k ++){
       key[k] = key[k+1];
       key[28+k] = key[29+k];
     }  
     key[27]=tempLeft;
     key[55]=tempRight;
   }
   var tempKey = new Array(48);
   tempKey[ 0] = key[13];
   tempKey[ 1] = key[16];
   tempKey[ 2] = key[10];
   tempKey[ 3] = key[23];
   tempKey[ 4] = key[ 0];
   tempKey[ 5] = key[ 4];
   tempKey[ 6] = key[ 2];
   tempKey[ 7] = key[27];
   tempKey[ 8] = key[14];
   tempKey[ 9] = key[ 5];
   tempKey[10] = key[20];
   tempKey[11] = key[ 9];
   tempKey[12] = key[22];
   tempKey[13] = key[18];
   tempKey[14] = key[11];
   tempKey[15] = key[ 3];
   tempKey[16] = key[25];
   tempKey[17] = key[ 7];
   tempKey[18] = key[15];
   tempKey[19] = key[ 6];
   tempKey[20] = key[26];
   tempKey[21] = key[19];
   tempKey[22] = key[12];
   tempKey[23] = key[ 1];
   tempKey[24] = key[40];
   tempKey[25] = key[51];
   tempKey[26] = key[30];
   tempKey[27] = key[36];
   tempKey[28] = key[46];
   tempKey[29] = key[54];
   tempKey[30] = key[29];
   tempKey[31] = key[39];
   tempKey[32] = key[50];
   tempKey[33] = key[44];
   tempKey[34] = key[32];
   tempKey[35] = key[47];
   tempKey[36] = key[43];
   tempKey[37] = key[48];
   tempKey[38] = key[38];
   tempKey[39] = key[55];
   tempKey[40] = key[33];
   tempKey[41] = key[52];
   tempKey[42] = key[45];
   tempKey[43] = key[41];
   tempKey[44] = key[49];
   tempKey[45] = key[35];
   tempKey[46] = key[28];
   tempKey[47] = key[31];
   switch(i){
     case 0: for(m=0;m < 48 ;m++){ keys[ 0][m] = tempKey[m]; } break;
     case 1: for(m=0;m < 48 ;m++){ keys[ 1][m] = tempKey[m]; } break;
     case 2: for(m=0;m < 48 ;m++){ keys[ 2][m] = tempKey[m]; } break;
     case 3: for(m=0;m < 48 ;m++){ keys[ 3][m] = tempKey[m]; } break;
     case 4: for(m=0;m < 48 ;m++){ keys[ 4][m] = tempKey[m]; } break;
     case 5: for(m=0;m < 48 ;m++){ keys[ 5][m] = tempKey[m]; } break;
     case 6: for(m=0;m < 48 ;m++){ keys[ 6][m] = tempKey[m]; } break;
     case 7: for(m=0;m < 48 ;m++){ keys[ 7][m] = tempKey[m]; } break;
     case 8: for(m=0;m < 48 ;m++){ keys[ 8][m] = tempKey[m]; } break;
     case 9: for(m=0;m < 48 ;m++){ keys[ 9][m] = tempKey[m]; } break;
     case 10: for(m=0;m < 48 ;m++){ keys[10][m] = tempKey[m]; } break;
     case 11: for(m=0;m < 48 ;m++){ keys[11][m] = tempKey[m]; } break;
     case 12: for(m=0;m < 48 ;m++){ keys[12][m] = tempKey[m]; } break;
     case 13: for(m=0;m < 48 ;m++){ keys[13][m] = tempKey[m]; } break;
     case 14: for(m=0;m < 48 ;m++){ keys[14][m] = tempKey[m]; } break;
     case 15: for(m=0;m < 48 ;m++){ keys[15][m] = tempKey[m]; } break;
   }
 }
 return keys;  
}"""

        # des_params = execjs.compile(functionStrEnc).call('strEnc', params, "9261531709014202222", "", "")
        des_params = execjs.compile(functionStrEnc).call('strEnc', params, self.__deskey, "", "")
        _params = base64.b64encode(str.encode(des_params))
        # 转回str
        _params = str(_params)
        _params = "params=" + _params.split("'")[1] + "&token="+token+"&timestamp="+self.__nowtime
        _webRootPath = "http://" + self.__nowUrl
        url = _webRootPath + "/student/xscj.stuckcj_data.jsp?" + _params
        headers = {'Host': self.__nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Referer': 'http://'+self.__nowUrl+'/student/xscj.stuckcj.jsp?menucode=JW130705',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID='+self.__sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        s = requests.session()
        s.headers.update(headers)
        try:
            r = s.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            informationlist = []
            for tbodys in soup.find_all(re.compile("^tbody")):
                for tbody in tbodys:
                    if tbody != '\n':
                        if tbody != '\n':
                            tds = tbody('td')
                            informationlist.append([tds[1].string, tds[2].string, tds[4].string, tds[6].string])
        except :
            print("暂无分数数据or接口拒绝访问，请重试")

        return informationlist

    # 选课查询，按学号
    def SelectClassByNumber(self):
        # xn = 2017
        # xq = "夏季学期"
        # xh = "16020031016"
        # 夏季学期 0 秋季 1 春季 2
        number = input("请输入你要查询的学号")
        params = "xn="+self.__xn+"&xq="+self.__xq+"&xh="+number
        # str to bytes
        params = str.encode(params)
        baseparams = base64.b64encode(params)
        # 转化bytes to str
        baseparams = bytes.decode(baseparams)
        strurl = "http://"+self.__nowUrl+"/wsxk/xkjg.ckdgxsxdkchj_data.jsp?params="+baseparams
        headers = {'Host': self.__nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type':'application/x-www-form-urlencoded',
                   'Referer': 'http://'+self.__nowUrl+'/student/xkjg.wdkb.jsp?menucode=JW130416',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + self.__sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        s = requests.session()
        s.headers.update(headers)
        r = s.get(strurl)
        soup = BeautifulSoup(r.text, "html.parser")
        informationlist = []
        try:
            for tr in soup.find('tbody').children:
                # 出现/n情况，/n在soup中被认为是子节点之一
                if tr != '\n':
                    tds = tr('td')
                    informationlist.append([tds[0].string, tds[1].string, tds[8].string])
            for i in range(len(informationlist)):
                information = informationlist[i]
                print("{:^10}\t{:^6}\t{:^10}".format(information[0], information[1], information[2]))
        except AttributeError as e:
            print("暂无选课数据")

    # 由SelectClassByClass调用
    @staticmethod
    def SelectClassByClass_UseNumber(xn, xq, nowUrl, sessionid, StuNum, ClassNum):
        # 夏季学期 0 秋季 1 春季 2
        params = "xn="+xn+"&xq="+xq+"&xh=" + StuNum
        # str to bytes
        params = str.encode(params)
        baseparams = base64.b64encode(params)
        # 转化bytes to str
        baseparams = bytes.decode(baseparams)
        strurl = "http://"+nowUrl+"/wsxk/xkjg.ckdgxsxdkchj_data.jsp?params=" + baseparams
        headers = {'Host': nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'http://'+nowUrl+'/student/xkjg.wdkb.jsp?menucode=JW130416',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        r = requests.get(strurl, headers=headers)
        # s.headers.update(headers)
        # r = s.get(strurl)
        soup = BeautifulSoup(r.text, "html.parser")
        informationlist = []
        try:
            for tr in soup.find('tbody').children:
                # 出现/n情况，/n在soup中被认为是子节点之一
                if tr != '\n':
                    tds = tr('td')
                    informationlist.append([tds[0].string, tds[1].string, tds[4].string, tds[8].string])
        except:
            print(soup)
            print(xn, xq, nowUrl, sessionid, StuNum, ClassNum)
        for i in range(len(informationlist)):
            information = informationlist[i]
            # information[0]存的是选课号，information[1]存的是课程名称，information[2]存的是是否重修,information[3]存的是选课币数量
            if information[0] == ClassNum:
                return information[3], information[2]
            # print("{:^10}\t{:^6}\t{:^10}".format(information[0], information[1], information[2]))

    # 查询年级专业所有学生
    def getAllStudentGrade(self):
        url = "http://" + self.__nowUrl + "/taglib/DataTable.jsp?tableId=3241"
        headers = { 'Host': self.__nowUrl,
                    'Connection': 'keep-alive',
                    'Content-Length': '262',
                    'Cache-Control': 'max-age=0',
                    'Origin': 'http://'+ self.__nowUrl,
                    'Upgrade-Insecure-Requests': '1',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Referer': 'http://'+self.__nowUrl+'/common/popmsg/popmsg.sendOnlineMessage.jsp',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cookie': 'JSESSIONID=' + self.__sessionid,
                    }
        nj = "2016"
        # print("选择院(系)/部\n1.[3001]海洋与大气学院\n2.[3002]信息科学与工程学院\n3.[3003]化学化工学院\n4.[3004]海洋地球科学学院\n"
        #       "5.[3005]海洋生命学院\n6.[3006]水产学院\n7.[3007]食品科学与工程学院\n8.[3008]医药学院\n9.[3009]工程学院\n"
        #       "10.[3010]环境科学与工程学院\n11.[3011]管理学院\n12.[3012]经济学院\n13.[3013]外国语学院\n14.[3014]文学与新闻传播学院\n"
        #       "15.[3015]法政学院\n16.[3016]数学科学学院\n17.[3017]材料科学与工程学院\n18.[3018]基础教学中心\n19.[3019]马克思主义学院\n")
        # choice = input("输入你的选择")
        # if choice == "1":
        #     yxbdm = "0048"
        # elif choice == "2":
        #     yxbdm = "0050"
        # elif choice == "3":
        #     yxbdm = "0051"
        # elif int(choice) > 3:
        #     yxbdm = 49 + int(choice)
        #     yxbdm = "00"+str(yxbdm)

        yxbdm = "0050"
        zydm = "0011"
        bjdm = "020031161"
        # 构造请求信息
        params = "hidOption=&hidKey=&userId="+self.__numberid+"&roletype=&jsrdm=&jsrmc=&nj="+nj+"&yhdm=&emptyFlag=0&xm=&xn=&xq=&" \
                 "style=STU&bmdm=&gradeController=on&nj2="+nj+"&yxbdm="+yxbdm+"&zydm="+zydm+"&bjdm="+bjdm+"&sel_role=ADM000&" \
                 "xnxq=2018-1&sel_skbjdm=&queryInfo=&_xxbt=&xxbt=&_xxnr=&xxnr=&fjmc="
        s = requests.session()
        s.headers.update(headers)
        r = s.post(url, data=params)
        soup = BeautifulSoup(r.text, "html.parser")
        informationlist = []
        try:
            for tr in soup.find('tbody').children:
                if tr != "\n":
                    tds = tr('td')
                    informationlist.append([tds[1].string, tds[2].string])
        except:
            print(" ")
        sortStudent = []
        for student in informationlist:
            gradelist = self.InquiryGrades("0000", "0", student[0], "0000-0")
            allGrade = 0 #成绩*学分
            allGrade2 = 0 #学分和
            allGrade3 = 0 #及格学分
            print(student[0])
            for grade in gradelist:
                if grade[3] != "良好" and grade[3] != "通过" and grade[3] != "中等" and grade[3] != "优秀" and not grade[3][0].isalpha():
                    allGrade = allGrade + float(grade[1])*float(grade[3])
                    allGrade2 = allGrade2 + float(grade[1])
                    if float(grade[1]) > 60:
                        allGrade3 = allGrade3 + float(grade[1])
            if int(float(allGrade2)) != 0:
                powerGrade = allGrade/allGrade2 + allGrade3*0.2
                sortStudent.append([student[0], student[1], powerGrade])

        def quickSort(L, low, high):
            i = low
            j = high
            if i >= j:
                return L
            key = L[i]
            while i < j:
                while i < j and float(L[j][2]) >= float(key[2]):
                    j = j - 1
                L[i] = L[j]
                while i < j and float(L[i][2]) <= float(key[2]):
                    i = i + 1
                L[j] = L[i]
            L[i] = key
            quickSort(L, low, i - 1)
            quickSort(L, j + 1, high)
            return L

        informationAboutGrade = quickSort(sortStudent, 0, len(sortStudent) - 1)
        for i in range(len(informationAboutGrade)):
            information = informationAboutGrade[len(informationAboutGrade) - 1 - i]
            print("{:^10}\t{:^10}\t{:^10}\t{:^10}".format(i + 1, information[0], information[1], information[2]))

    # 获取给分情况
    def getClassGrade(self):
        headers = {'Host': self.__nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type':'application/x-www-form-urlencoded',
                   'Referer': 'http://'+self.__nowUrl+'/common/popmsg/popmsg.sendOnlineMessage.jsp',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + self.__sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        # sel_skbjdm = "02003011"
        sel_skbjdm = input("请输入选课号")
        # 构造请求信息
        params = "hidOption= &hidKey=&userId="+self.__numberid+"&roletype=&jsrdm=&jsrmc=&nj="+self.__xn+"&" \
                "yhdm=&emptyFlag=0&xm=& xn=&xq=&style=SKBJDM&bmdm=&gradeController=on&" \
                "nj2="+self.__xn+"&yxbdm=&sel_role=ADM000&xnxq= "+self.__xn+"-"+self.__xq+"&sel_skbjdm="+sel_skbjdm+"&" \
                "queryInfo=&_xxbt=&xxbt=&_xxnr=&xxnr=& fjmc="
        url = "http://"+self.__nowUrl+"/taglib/DataTable.jsp?tableId=3241&type=skbjdm"
        s = requests.session()
        s.headers.update(headers)
        r = s.post(url, data=params)
        soup = BeautifulSoup(r.text, "html.parser")
        # 选该课人员
        studentinformationlist = []
        try:
            for tr in soup.find('tbody').children:
                if tr.name != "input":
                    tds = tr('td')
                    studentinformationlist.append([tds[1].string, tds[2].string, tds[3].string, tds[5].string])
        except:
            print("暂无数据，请重试")

        params = "xn=" + self.__xn + "&xq=" + self.__xq + "&xh=" + studentinformationlist[0][0]
        # str to bytes
        params = str.encode(params)
        baseparams = base64.b64encode(params)
        # 转化bytes to str
        baseparams = bytes.decode(baseparams)
        strurl = "http://" + self.__nowUrl + "/wsxk/xkjg.ckdgxsxdkchj_data.jsp?params=" + baseparams
        headers = {'Host': self.__nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': 'http://' + self.__nowUrl + '/student/xkjg.wdkb.jsp?menucode=JW130416',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + self.__sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        s = requests.session()
        s.headers.update(headers)
        r = s.get(strurl)
        soup = BeautifulSoup(r.text, "html.parser")
        className = ""
        informationlist = []
        try:
            for tr in soup.find('tbody').children:
                # 出现/n情况，/n在soup中被认为是子节点之一
                if tr != '\n':
                    tds = tr('td')
                    informationlist.append([tds[0].string, tds[1].string, tds[8].string])
            for i in range(len(informationlist)):
                information = informationlist[i]
                if information[0] == sel_skbjdm:
                    className = information[1]
                    break
                # print("{:^10}\t{:^6}\t{:^10}".format(information[0], information[1], information[2]))
        except AttributeError as e:
            print("暂无选课数据")

        score = []
        for student in studentinformationlist:
            gradelist = self.InquiryGrades("0000", "0", student[0], "0000-0")
            for grade in gradelist:
                if grade[0] == className:
                    print(student[0])
                    score.append([student[0], student[1], grade[3]])

        def quickSort(L, low, high):
            i = low
            j = high
            if i >= j:
                return L
            key = L[i]
            while i < j:
                while i < j and float(L[j][2]) >= float(key[2]):
                    j = j - 1
                L[i] = L[j]
                while i < j and float(L[i][2]) <= float(key[2]):
                    i = i + 1
                L[j] = L[i]
            L[i] = key
            quickSort(L, low, i - 1)
            quickSort(L, j + 1, high)
            return L

        score = quickSort(score, 0, len(score) - 1)
        for i in range(len(score)):
            information = score[len(score) - 1 - i]
            print("{:^10}\t{:^10}\t{:^10}\t{:^10}".format(i + 1, information[0], information[1], int(float(information[2]))))
        numlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(score)):
            information = score[len(score) - 1 - i]
            local = int(int(float(information[2]))/10)
            numlist[local] = numlist[local] + 1

        # rects = plt.bar(range(len(numlist)), numlist, color='rgby')
        # name_list = ['>=0', '>=10', '>=20', '>=30', '>=40', '>=50', '>=60', '>=70', '>=80', '>=90']
        # plt.xticks(range(len(numlist)), name_list)
        # plt.ylabel("人数")
        # for rect in rects:
        #     height = rect.get_height()
        #     plt.text(rect.get_x() + rect.get_width() / 2., 1.03 * height, '%s' % float(height))
        # plt.show()
    # 选课查询，按课程
    def SelectClassByClass(self):
        headers = {'Host': self.__nowUrl,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                   'Accept-Encoding': 'gzip, deflate',
                   'Content-Type':'application/x-www-form-urlencoded',
                   'Referer': 'http://'+self.__nowUrl+'/common/popmsg/popmsg.sendOnlineMessage.jsp',
                   'Content-Length': '824',
                   'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + self.__sessionid,
                   'Upgrade-Insecure-Requests': '1'}
        # sel_skbjdm = "02003011"
        sel_skbjdm = input("请输入选课号")
        # 构造请求信息
        params = "hidOption= &hidKey=&userId="+self.__numberid+"&roletype=&jsrdm=&jsrmc=&nj="+self.__xn+"&" \
                "yhdm=&emptyFlag=0&xm=& xn=&xq=&style=SKBJDM&bmdm=&gradeController=on&" \
                "nj2="+self.__xn+"&yxbdm=&sel_role=ADM000&xnxq= "+self.__xn+"-"+self.__xq+"&sel_skbjdm="+sel_skbjdm+"&" \
                "queryInfo=&_xxbt=&xxbt=&_xxnr=&xxnr=& fjmc="
        url = "http://"+self.__nowUrl+"/taglib/DataTable.jsp?tableId=3241&type=skbjdm"
        s = requests.session()
        s.headers.update(headers)
        r = s.post(url, data=params)
        soup = BeautifulSoup(r.text, "html.parser")
        informationlist = []
        informationAboutClass = []
        try:
            for tr in soup.find('tbody').children:
                if tr.name != "input":
                    tds = tr('td')
                    informationlist.append([tds[1].string, tds[2].string, tds[3].string, tds[5].string])

            # 多线程查询，信息表，选课号，线程数
            n_thread = int(input("输入线程数（不建议过大=。=）："))
            q = Thread.processSelect(self.__xn, self.__xq, self.__nowUrl, self.__sessionid, informationlist, sel_skbjdm, n_thread)
            while not q.empty():
                informationAboutClass.append(q.get())
            # 单线程查询
            # countOfLose = 0
            # for i in range(len(informationlist)):
            #     try:
            #         information = informationlist[i]
            #         # print("{:^10}\t{:^6}\t{:^10}".format(information[0], information[1], information[2]))
            #         moneyOfClass, ifReStudy = self.SelectClassByClass_UseNumber(self.__xn, self.__xq, self.__nowUrl, self.__sessionid, information[0], sel_skbjdm)
            #         powerOfCoin = moneyOfClass
            #         print(int(str(information[0])))
            #         if(int(str(information[0])) >= 17000000000 and int(str(information[0]))< 18000000000):
            #             powerOfCoin = int(str(moneyOfClass))*1
            #         if (int(str(information[0])) >= 16000000000 and int(str(information[0])) < 17000000000):
            #             powerOfCoin = int(str(moneyOfClass))*1.1
            #         if (int(str(information[0])) >= 15000000000 and int(str(information[0])) < 16000000000):
            #             powerOfCoin = int(str(moneyOfClass))*1.2
            #         if (int(str(information[0])) >= 14000000000 and int(str(information[0])) < 15000000000):
            #             powerOfCoin = int(str(moneyOfClass))*1.3
            #         informationAboutClass.append([powerOfCoin, moneyOfClass, ifReStudy, information[0], information[1], information[2]])
            #     except urllib.request.HTTPError as e:
            #         countOfLose += 1
            #         print("丢失数据:")
            #         print(countOfLose)
            #         print("\n")
            #         print(e.code)
            #         print(e.reason)

            def quickSort(L, low, high):
                i = low
                j = high
                if i >= j:
                    return L
                key = L[i]
                while i < j:
                    while i < j and int(str(L[j][1])) >= int(str(key[1])):
                        j = j-1
                    L[i] = L[j]
                    while i < j and int(str(L[i][1])) <= int(str(key[1])):
                        i = i+1
                    L[j] = L[i]
                L[i] = key
                quickSort(L, low, i-1)
                quickSort(L, j+1, high)
                return L
            informationAboutClass = quickSort(informationAboutClass, 0, len(informationAboutClass)-1)

            for i in range(len(informationAboutClass)):
                information = informationAboutClass[len(informationAboutClass)-1-i]
                print("{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}".format(i+1, information[0], information[1], information[2], information[3], information[4], information[5]))
            print("总共丢失数据:")
            # print(countOfLose)
            print("\n")
        except AttributeError as e:
            print("暂无选课数据")

    @staticmethod
    def acquirePhoto():
        studentNumber = int(input("请输入你的学号"))
        # 1026是16级和之前的
        if studentNumber > 17000000000:
            time = "20170815"
        else:
            time = "20161026"
        strStudentNumber = str(studentNumber)
        url = "http://hqxsgy.ouc.edu.cn/uploadfile/image/photos/" + time + "/" + strStudentNumber + ".jpg"
        r = requests.get(url)
        name = strStudentNumber + ".jpg"
        with open(name, "wb") as fp:
            fp.write(r.content)
        print("操作成功！")
