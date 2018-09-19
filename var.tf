variable "AWS_REGION" {default="us-east-1"}
variable "AMIS" {
    type= "map"
    default={
        us-east-1="ami-0d729a60"
        us-west-2="ami-06b94666"
    }
}
variable "PATH_TO_PRIVATE_KEY" {}
variable "instance" {}
variable "PATH_TO_PUBLIC_KEY" {}
variable "Instance_Username" {}