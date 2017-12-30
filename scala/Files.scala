import java.io.File

import scala.annotation.tailrec
import scala.collection.JavaConverters._

class Files(path: String, session: String)
{
    val file = new File(path)
    val outputpath = s"$session-unpacked"
    val folder = new File(outputpath)
    // We want a fresh directory!
    if (folder.exists()) for (f <- folder.listFiles()) f.delete()
    else folder.mkdir()
    folder.deleteOnExit()

    val zip = ZipFile(file, outputpath)
    @tailrec
    private final def unpack(zip: ZipFile, files: List[String] = Nil): List[String] = zip match
    {
        case zip :< file => unpack(zip, file::files)
        case unzipped => files
    }
    val fileList: List[String] = unpack(zip)
    def files(): java.util.List[String] = fileList.asJava
}