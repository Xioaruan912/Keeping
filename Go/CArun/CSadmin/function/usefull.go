
package function

import (
	"bufio"
	"math/rand"
	"os"
	"time"
)

func Scanf(a *string) {
	reader := bufio.NewReader(os.Stdin)
	data, _, _ := reader.ReadLine()

	*a = string(data)
}

func RandNum() int {
	rand.Seed(time.Now().UnixNano()) //时间戳为种子
	r := rand.Intn(65535)
	return r
}
