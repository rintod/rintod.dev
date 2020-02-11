package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
)

const (
	Green = "\033[1;32m>>\033[0m"
	Red   = "\033[1;31m>>\033[0m"
)

// BUILD WITH LOVE BY rintod.dev
// GITHUB.COM/rintod
func main() {
emailList:
	lists := bufio.NewReader(os.Stdin)
	fmt.Print("List: ")
	req, _ := lists.ReadString('\n')
	stdout := strings.Replace(req, "\n", "", -1)
	if _, err := os.Stat(stdout); os.IsNotExist(err) {
		fmt.Println("File Not Exits")
		goto emailList
	}
	file, err := os.Open(stdout)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	listss := bufio.NewScanner(file)
	for listss.Scan() {
		email := listss.Text()
		checkEmail(email)
	}
}
func checkEmail(email string) {
	server, err := net.Dial("tcp", "gmail-smtp-in.l.google.com:25")
	if err != nil {
		log.Fatal(err)
	}
	_, errs := bufio.NewReader(server).ReadString('\n')
	if errs != nil {
		log.Fatal(errs)
	}
	fmt.Fprintf(server, "EHLO rintod.dev\r\n")
	msg, err := bufio.NewReader(server).ReadString('\n')
	if err != nil {
		log.Fatal(err)
	}
	if msg[:3] != "250" {
		log.Fatal("Cant Send EHLO To Server")
	}
	fmt.Fprintf(server, "MAIL FROM: <root@rintod.dev>\r\n")
	mailfrom, errr := bufio.NewReader(server).ReadString('\n')
	if errr != nil {
		log.Fatal(errr)
	}
	if mailfrom[:3] != "250" {
		log.Fatal("Cant Set MAIL FROM")
	}
	fmt.Fprintf(server, "RCPT TO: <"+email+">\r\n")
	Valid, errrr := bufio.NewReader(server).ReadString('\n')
	if errrr != nil {
		log.Fatal()
	}
	if Valid[:3] != "250" {
		fmt.Println(Red, email, "Is Not Valid")
	} else {
		fmt.Println(Green, email, "Is Valid")
		mkFile("valid.txt", email)
	}
}

func mkFile(filename string, content string) {
	var NewContent = content + "\n"
	file, err := os.OpenFile(filename, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	if _, err := file.Write([]byte(NewContent)); err != nil {
		log.Fatal(err)
	}
	if err := file.Close(); err != nil {
		log.Fatal(err)
	}
}
