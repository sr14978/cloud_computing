import sys.process._
import Compiler._

import scala.util.Try

case class Compiler(flags_ : Flags)
{
    val Flags(_, compiler, flags, _) = flags_
    def apply(filename: String): Result =
    {
        println(s"compiling $filename")
        val objectname = filename.split('.').head + ".o"
        var out = ""
        Try(s"$compiler -c $filename -o $objectname $flags" !! ProcessLogger(line => out += line + "\n")) match
        {
            case scala.util.Success(_) => Success(objectname, GCCParser(out))
            case scala.util.Failure(_) => Error(GCCParser(out))(filename)
        }
    }
}

object Compiler
{
    sealed trait Result
    {
        val filename: String
    }
    case class Success(filename: String, warnings: List[String]) extends Result
    case class Error(msgs: List[String])(val filename: String) extends Result
}
