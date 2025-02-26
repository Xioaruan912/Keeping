package upload

import (
	"io"
	"net"
	"os"
	"path/filepath"
)

func CheckFile(file string) string {
	_, err := os.Open(file)
	if err != nil {
		return "no"
	} else {
		return "yes"
	}
}

func CheckFileName(file string) string {
	filename := filepath.Base(file)
	return filename
}

func Write_File_toconn(file string, conn net.Conn) string {
	buf := make([]byte, 20*50*1024*1024)
	files, err := os.Open(file)
	if err != nil {
		return "文件不存在"
	}
	for {
		n, err := files.Read(buf)
		if err == io.EOF {
			return "读取完毕"
		}
		_, _ = conn.Write(buf[:n])

	}
}
