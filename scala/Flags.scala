import scala.collection.breakOut

case class Flags(exename: String, compiler: String, fcompile: String, flink: String)
object Flags
{
    def apply(zipname: String, args: Array[String]): Flags =
    {
        val map: Map[String, String] = (for (arg <- args; if arg.contains("="); (key, value) = arg.span(_!='=')) yield key -> value.tail)(breakOut)
        val exename = map.getOrElse("exename", zipname.split('.').head)
        // If the compiler isn't specified we should default to g++ to be on the safe side
        val compiler = map.getOrElse("compiler", "g++")
        val fcompile = map.getOrElse("compiler-flags", "")
        val flink = map.getOrElse("linker-flags", "")
        new Flags(exename, compiler, fcompile, flink)
    }
}
