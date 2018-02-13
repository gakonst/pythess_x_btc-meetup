// Simple Crowdfunding Contract
pragma solidity ^0.4.19;

contract Crowdfunding {
  
  event Contributed(address _sender, uint amount);

  uint public crowdSaleDuration;
  uint public crowdSaleStart;
  uint public crowdSaleGoal;
  uint public amountRaised;
  address public owner;

  mapping (address => uint) public contributions;
  
  function Crowdfunding(uint256 _crowdSaleDuration, uint _crowdSaleGoal) public {
    crowdSaleDuration = _crowdSaleDuration;
    crowdSaleStart = now;
    crowdSaleGoal = _crowdSaleGoal;
    owner = msg.sender;
  }

  function ownerWithdraw() public {
    require(now >= crowdSaleStart + crowdSaleDuration && this.balance >= crowdSaleGoal);
    require(msg.sender == owner);

    owner.transfer(this.balance);
  }

  function withdraw() public {  
    require(now >= crowdSaleStart + crowdSaleDuration && this.balance >= crowdSaleGoal);

    uint amount = contributions[msg.sender];
    contributions[msg.sender] = 0;
    msg.sender.transfer(amount);
  }

  function contribute() payable public{
    require(msg.value + amountRaised <= crowdSaleGoal);
    require(now < crowdSaleStart + crowdSaleDuration);
    contributions[msg.sender] += msg.value;
    amountRaised += msg.value;
  }

  function() payable public {
    contribute();
  }

}
