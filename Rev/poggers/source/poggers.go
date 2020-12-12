package main

import (
	"encoding/base64"
	"fmt"
	"math/bits"
	"os"
	"path/filepath"
	"strings"
)

func sus(s string) string {
	v0 := ""
	v1 := ""
	for i := 0; i < len(s); i++ {
		if i % 2 == 0 {
			v0 += string(s[len(s) - i - 1])
		} else {
			v1 += string(s[len(s) - i - 1])
		}
	}
	return v0 + v1
}

func string2uint64(s string) uint64 {
	pan := []byte(s)
	var res uint64
	res = 0
	for j := 0; j < 8; j++ {
		res |= uint64(pan[j])
		if j != 7 {
			res <<= 8
		}
	}
	return res
}

func pad8(s string) string {
	tun := "!@#$%^&*"
	if len(s) % 8 != 0 {
		s = s + strings.Repeat(string(tun[8 - (len(s) % 8)]), 8 - (len(s) % 8))
	}
	return s
}

func poggers(s string) string {
	s = sus(pad8(s))
	res := []byte(s)
	var tmp uint64
	for i := 0; i < len(s); i += 8 {
		tmp = string2uint64(s[i:i + 8])
		tmp = tmp ^ (tmp >> 1)
		tmp = bits.RotateLeft64(tmp, 13)
		for j := 0; j < 8; j++ {
			res[i + j] = byte(((tmp >> uint64(8 * j)) ^ 0x69) & 0xFF)
		}
	}
	return base64.StdEncoding.EncodeToString(res)
}

func main() {
	if len(os.Args) == 2 {
		fmt.Printf("%s\n", poggers(filepath.Base(os.Args[1])))
	} else {
		fmt.Printf("Usage: %s <string>\n", os.Args[0])
	}
}
