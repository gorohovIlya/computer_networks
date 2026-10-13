import kotlin.text.Regex
import java.util.Scanner
import java.io.File

fun main() {
    val macRegex = Regex("[0-9A-F]{2}(-[0-9A-F]{2}){5}")
    val scanner = Scanner(System.`in`)
    println("Введите MAC-адрес в формате F0-79-59-70-A7-20")
    val macAddressStr = scanner.nextLine().uppercase()
    if (!macRegex.matches(macAddressStr)) {
        println("Некорректный формат MAC-адреса!")
    }
    val macAddressBytes = macAddressStr.split("-")
    val file = File("mac-vendor.txt")
    val lines = file.readLines()
    val first3bytes = macAddressBytes[0] + macAddressBytes[1] + macAddressBytes[2]
    val macAddressMap: Map<String, String> = lines.associate {
        item -> item.split("\t")[0] to item.split("\t")[1]
    }
    val producer: String? = macAddressMap[first3bytes]
    if (producer != null) {
        println("Производитель: ${macAddressMap[first3bytes]}")
    }
    else {
        println("Производителя с кодом $producer не существует")
    }
}