resource "aws_key_pair" "mykey" {
  key_name="mykey"
  public_key="${file("${var.PATH_TO_PUBLIC_KEY}")}"
}

resource "aws_instance" "example" {
  ami           = "${lookup(var.AMIS,var.AWS_REGION)}"
  instance_type = "${(var.instance)}"
  key_name = "${aws_key_pair.mykey.key_name}"

  provisioner "file" {
    source="script.sh"
    destination = "/tmp/script.sh"
  }

  provisioner "remote-exec" {
    inline=["chmod +x /tmp/script.sh","sudo /tmp/script.sh"]
  }
  connection {
    user = "${var.Instance_Username}"
    private_key = "${file("${var.PATH_TO_PRIVATE_KEY}")}"
  }
  }