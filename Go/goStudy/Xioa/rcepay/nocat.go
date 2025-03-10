package rcepay

import (
	"fmt"
	"os"
	"text/tabwriter"
)

func Nocat1() {
	var nocat = [][]string{
		{"tac", "more", "less", "head", "tail", "nl", "od", "paste", "sort", "curl", "c'at'", "c\"at\"", "c``at", "c\\at", "sh /flag 2>%261", "uniq", "vim", "vi", "a=fl;b=ag;cat$IFS$a$b", "\\bin\\?at"},
		{"https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.cnblogs.com/machangwei-8/p/9570550.html", "https://www.runoob.com/linux/linux-comm-od.html", "https://www.runoob.com/linux/linux-comm-paste.html", "https://www.runoob.com/linux/linux-comm-sort.html", "https://www.ruanyifeng.com/blog/2019/09/curl-reference.html", "https://blog.csdn.net/weixin_46270220/article/details/113695350", "https://blog.csdn.net/weixin_46270220/article/details/113695350", "https://blog.csdn.net/weixin_46270220/article/details/113695350", "https://blog.csdn.net/weixin_46270220/article/details/113695350", "https://blog.csdn.net/weixin_46706771/article/details/119031475", "https://www.runoob.com/linux/linux-comm-uniq.html", "https://www.runoob.com/linux/linux-vim.html", "https://www.runoob.com/linux/linux-vim.html", "https://zhuanlan.zhihu.com/p/338967809", "https://blog.csdn.net/weixin_46270220/article/details/113695350"},
	}

	w := tabwriter.NewWriter(os.Stdout, 0, 0, 1, ' ', tabwriter.TabIndent)

	for j := 0; j < len(nocat[0]); j++ {
		fmt.Fprintf(w, "\x1b[31m%d\x1b[0m\t%s\t\t\t\t%s\t\x1b[0m\n", j, nocat[0][j], nocat[1][j])
	}

	w.Flush()
}
