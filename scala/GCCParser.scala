object GCCParser
{
    // This can get much more advanced, including actually packaging the errors and warnings up
    def apply(msgs: String): List[String] =
    {
        if (msgs.isEmpty) Nil
        else msgs.split('\n').toList
    }
}
