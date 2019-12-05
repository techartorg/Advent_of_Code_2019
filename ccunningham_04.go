package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

var digits = []rune("0123456789")

func main() {
	possibleCount := 0
	filteredCount := 0

	for i := 130254; i < 678275; i++ {
		v := strconv.Itoa(i)

		vSorted := []rune(v); sort.Slice(vSorted, func(i, j int) bool {
			return vSorted[i] < vSorted[j]
		})

		if v != string(vSorted) {
			continue
		}

		hasPair := false
		for _, d := range digits {
			if strings.Count(v, string(d)) > 1 {
				hasPair = true
				break
			}
		}

		if hasPair {
			possibleCount++
		}

		for _, d := range digits {
			if strings.Count(v, string(d)) == 2 {
				filteredCount++
				break
			}
		}
	}

	fmt.Printf("Part 01: %v\n", possibleCount)
	fmt.Printf("Part 02: %v\n", filteredCount)
}
