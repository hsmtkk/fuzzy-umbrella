import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as docdb from 'aws-cdk-lib/aws-docdb';
import * as ec2 from 'aws-cdk-lib/aws-ec2';

export class CdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = ec2.Vpc.fromLookup(this, "vpc", {
      isDefault: true,
    })

    const securityGroup = new ec2.SecurityGroup(this, "securityGroup", {
      vpc: vpc,
      allowAllOutbound: true,
    })

    securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(27017),
      "MongoDB")

    const cluster = new docdb.DatabaseCluster(this, "cluster", {
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM),
      masterUser: {
        excludeCharacters: '\"@/:$<>[](){},.%!=`#?*&|\'^~\\;+',
        username: "master"
      },
      securityGroup: securityGroup,
      vpc: vpc,
    });

  }
}
