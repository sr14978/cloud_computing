import java.io.File

import sys.process._
import Linker._

import scala.collection.JavaConverters._
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

    def link(objects: java.util.List[String]): String =
    {
        this(for (objstr <- objects.asScala.toList) yield Compiler.Result.unpickle(objstr)).pickle()
    }
}

object Linker
{
    sealed trait Result
    {
        def pickle(): String
    }
    object Result
    {
        def unpickle(pickle: String): Result = (pickle.split('\u0007').toList: @unchecked) match
        {
            case "S"::exename::warnings => Success(exename, warnings)
            case "F"::errors => Failure(errors)
        }
    }
    case class Success(exename: String, warnings: List[String]) extends Result
    {
        def pickle() = s"S\u0007${exename}\u0007${warnings.mkString("\u0007")}"
        def getWarnings() = warnings.asJava
    }
    case class Failure(errors: List[String]) extends Result
    {
        def pickle() = s"F\u0007${errors.mkString("\u0007")}"
        def getErrors() = errors.asJava
    }
}
