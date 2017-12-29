import java.io.{File, FileInputStream, FileOutputStream}
import java.util.zip.{ZipEntry, ZipInputStream}

import scala.annotation.tailrec

case class ZipFile(file: File, val outputpath: String)
{
    val zip = new ZipInputStream(new FileInputStream(file))
    def next() = Option(zip.getNextEntry)
    @tailrec
    final def >>(fos: FileOutputStream)(implicit buf: Array[Byte] = new Array[Byte](1024)): Unit =
    {
        val nread = zip.read(buf)
        if (nread > 0)
        {
            fos.write(buf, 0, nread)
            this >> fos
        }
    }
}

object :<
{
    def unapply(zip: ZipFile): Option[(ZipFile, String)] =
    {
        for (entry <- zip.next) yield
        {
            val filename = entry.getName()
            val file = new File(s"${zip.outputpath}${File.separator}$filename")
            println(s"unzipping: ${file.getPath}")
            val fos = new FileOutputStream(file)
            zip >> fos
            fos.close()
            file.deleteOnExit()
            (zip, file.getPath)
        }
    }
}