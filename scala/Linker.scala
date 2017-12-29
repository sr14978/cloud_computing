import java.io.File

import sys.process._
import Linker._

import scala.util.Try

case class Linker(session: String, flags_ : Flags)
{
    val Flags(exename, compiler, _, flags) = flags_
    def apply(objects: List[Compiler.Result]): Linker.Result =
    {
        type Errors = List[String]
        type Warnings = List[String]
        type Objects = List[String]
        val init: Either[Errors, (Objects, Warnings)] = Right(Nil, Nil)
        objects.foldLeft(init)
        {
            case (Left(errs), Compiler.Success(_, warnings)) => Left(errs ++ warnings)
            case (Left(errs), Compiler.Error(errs_)) => Left(errs ++ errs_)
            case (Right((objs, warnings)), Compiler.Success(obj, warnings_)) => Right(obj :: objs, warnings ++ warnings_)
            case (Right((_, warnings)), Compiler.Error(errs)) => Left(warnings ++ errs)
        } match
        {
            case Left(errs) => Failure(errs)
            case Right((objs, warnings)) =>
                var out = ""
                val attempt = Try(s"$compiler -o $session-$exename ${objs.mkString(" ")} $flags" !! ProcessLogger(line => out += line + "\n"))
                for (obj <- objs) new File(obj).delete()
                attempt match
                {
                    case scala.util.Success(_) => Success(exename, warnings ::: GCCParser(out))
                    case scala.util.Failure(_) => Failure(warnings ::: GCCParser(out))
                }
        }
    }
}

object Linker
{
    sealed trait Result
    case class Success(exename: String, warnings: List[String]) extends Result
    case class Failure(errors: List[String]) extends Result
}
