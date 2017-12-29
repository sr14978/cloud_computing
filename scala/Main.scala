import scala.concurrent.{Await, Future}
import scala.concurrent.duration._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.util.{Failure, Success}
import scala.language.postfixOps

object Main
{
    def main(args: Array[String]): Unit =
    {
        val sequential = false
        // first arg in main will be a zip file address, we need to unzip it
        args.headOption match
        {
            case Some(path) =>
                val sessionname = "session_" + scala.util.Random.nextInt()
                val flags = Flags(path, args.tail)
                val files = new Files(path, sessionname)
                val compiler = Compiler(flags)
                val linker = Linker(sessionname, flags)
                val fobjects =
                    if (sequential) Future(for (file <- files.fileList if !file.endsWith(".h")) yield compiler(file))
                    else Future.sequence(for (file <- files.fileList if !file.endsWith(".h")) yield Future(compiler(file)))
                val fexe = for (objects <- fobjects) yield linker(objects) match
                {
                    case Linker.Success(exename, Nil) => s"Compilation succeeded into [$exename] without warnings"
                    case Linker.Success(exename, warnings) => s"Compilation succeeded into [$exename] with warnings;\n${warnings.mkString("\n")}"
                    case Linker.Failure(errors) => "Compilation failed with errors;\n" + errors.mkString("\n")
                }
                fexe.onComplete
                {
                    case Success(msg) => println(msg)
                    case Failure(err) => err.printStackTrace()
                }
                Await.result(fexe, 5 minutes)
            case None => println("Please enter a valid zipfile and then optional arguments")
        }
    }
}
