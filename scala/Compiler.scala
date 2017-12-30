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
    def compile(filename: String): String = this(filename).pickle()
}

object Compiler
{
    sealed trait Result
    {
        val filename: String
        def pickle(): String
    }
    object Result
    {
        def unpickle(pickle: String): Result = (pickle.split('\u0007').toList: @unchecked) match
        {
            case "S"::filename::warnings => Success(filename, warnings)
            case "E"::filename::msgs => Error(msgs)(filename)
        }
    }
    case class Success(filename: String, warnings: List[String]) extends Result
    {
        def pickle() = s"S\u0007${filename}\u0007${warnings.mkString("\u0007")}"
    }

    case class Error(msgs: List[String])(val filename: String) extends Result
    {
        def pickle() = s"E\u0007${filename}\u0007${msgs.mkString("\u0007")}"
    }
